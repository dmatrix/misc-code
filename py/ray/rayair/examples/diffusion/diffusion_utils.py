import torch
import datasets
import diffusers
import accelerate 
import os
from tqdm import tqdm
from PIL import Image

import torch.nn.functional as F
import torchvision.transforms as T
from diffusers import UNet2DModel
from accelerate import Accelerator
from diffusers import DDPMPipeline
import torchvision.transforms as T
from typing import List, Any, Dict
from dataclasses import dataclass
from datasets import load_dataset
import matplotlib.pyplot as plt
from ray.train.torch import TorchCheckpoint
from ray.air import session
        
@dataclass
class TrainingConfig:
    image_size = 128  # the generated image resolution
    train_batch_size = 16
    eval_batch_size = 16  # how many images to sample during evaluation
    num_epochs = 20       # 100 is a good max
    gradient_accumulation_steps = 1
    learning_rate = 1e-4
    lr_warmup_steps = 500
    save_image_epochs = int(num_epochs / 2)     
    save_model_epochs = int(num_epochs / 2)
    mixed_precision = 'fp16'  # `no` for float32, `fp16` for automatic mixed precision
    output_dir = '/mnt/cluster_storage/ddpm-butterflies-128'  # save the mode on the Anyscale storage locally or on the HF Hub
 
    overwrite_output_dir = True  # overwrite the old model when re-running the notebook
    seed = 42
    push_to_hub = False  # whether to upload the saved model to the HF Hub
    hub_private_repo = False  
    overwrite_output_dir = True  # overwrite the old model when re-running the notebook

        
# load the data from an existing diffusion model
# We will use the 🤗 Datasets library to download our image dataset.
# In this case, the Butterflies dataset is hosted remotely, but you can load a 
# local ImageFolder.
def load_data(dataset_name: str) -> datasets.arrow_dataset.Dataset:
    dataset = load_dataset(dataset_name, split="train")
    return dataset

# Plot the dataset
def plot_data(ds: datasets.arrow_dataset.Dataset) -> None:
    fig, axs = plt.subplots(1, 4, figsize=(16, 4))
    #show four images
    for i, image in enumerate(ds[:4]["image"]):
        axs[i].imshow(image)
        axs[i].set_axis_off()
    fig.show()
    
def plot_image(image: torch.Tensor) -> None:
    fig, axs = plt.subplots(1, 1, figsize=(16, 4))
    axs[0].imshow(image)
    axs[0].set_axis_off()
    fig.show()
    
def plot_transformed_data(ds: datasets.arrow_dataset.Dataset) -> None:
    fig, axs = plt.subplots(1, 4, figsize=(16, 4))
    for i, image in enumerate(ds[:4]["images"]):
        axs[i].imshow(image.permute(1, 2, 0).numpy() / 2 + 0.5)
        axs[i].set_axis_off()
    fig.show()
    
def create_model(image_size: int) -> diffusers.models.unet_2d.UNet2DModel:

    model = UNet2DModel(
        sample_size=image_size,  # the target image resolution
        in_channels=3,           # the number of input channels, 3 for RGB images
        out_channels=3,          # the number of output channels
        layers_per_block=2,      # how many ResNet layers to use per UNet block
        block_out_channels=(128, 128, 256, 256, 512, 512),  # the number of output channes for each UNet block
        down_block_types=( 
            "DownBlock2D",  # a regular ResNet downsampling block
            "DownBlock2D", 
            "DownBlock2D", 
            "DownBlock2D", 
            "AttnDownBlock2D",  # a ResNet downsampling block with spatial self-attention
            "DownBlock2D",
        ), 
        up_block_types=(
            "UpBlock2D",  # a regular ResNet upsampling block
            "AttnUpBlock2D",  # a ResNet upsampling block with spatial self-attention
            "UpBlock2D", 
            "UpBlock2D", 
            "UpBlock2D", 
            "UpBlock2D"  
          ),
    )
    return model

import math

def make_grid(images, rows, cols):
    w, h = images[0].size
    grid = Image.new('RGB', size=(cols*w, rows*h))
    for i, image in enumerate(images):
        grid.paste(image, box=(i%cols*w, i//cols*h))
    return grid

def evaluate(config, epoch, pipeline):
    # Sample some images from random noise (this is the backward diffusion process).
    # The default pipeline output type is `List[PIL.Image]`
    images = pipeline(
        batch_size = config.eval_batch_size, 
        generator=torch.manual_seed(config.seed),
    )["sample"]

    # Make a grid out of the images
    image_grid = make_grid(images, rows=4, cols=4)

    # Save the images
    test_dir = os.path.join(config.output_dir, "samples")
    os.makedirs(test_dir, exist_ok=True)
    image_grid.save(f"{test_dir}/{epoch:04d}.png")

def training_worker_per_loop(tr_config: Dict) -> None:
    
    config = tr_config['config']
    preprocessor = T.Compose(
    [
        T.Resize((config.image_size, config.image_size)),
        T.RandomHorizontalFlip(),
        T.ToTensor(),
        T.Normalize([0.5], [0.5]),
    ])
    
    def transform(examples: List[torch.tensor]) -> Dict[Any, Any]:
        images = [preprocessor(image.convert("RGB")) for image in examples["image"]]
        return {"images": images}
    
    # Initialize accelerator and tensorboard logging and metrics
    metrics = dict(train_loss=[])
    accelerator = Accelerator(
         mixed_precision=config.mixed_precision,
         gradient_accumulation_steps=config.gradient_accumulation_steps, 
         log_with="tensorboard",
         logging_dir=os.path.join(config.output_dir, "logs")
    )
    if accelerator.is_main_process:
        accelerator.init_trackers("train_example")
    
    config.dataset = "huggan/smithsonian_butterflies_subset"
    dataset = load_dataset(config.dataset, split="train")
    dataset.set_transform(transform)
    
    tr_dataloader = torch.utils.data.DataLoader(dataset, batch_size=config.train_batch_size, shuffle=True)
    
    # Prepare everything
    # There is no specific order to remember, you just need to unpack the 
    # objects in the same order you gave them to the prepare method.
    model, optimizer, train_dataloader, lr_scheduler = accelerator.prepare(
        config.model, config.optimizer, tr_dataloader, config.lr_scheduler
    )
    global_step = 0
    
    # Now you train the model
    for epoch in range(config.num_epochs):
        progress_bar = tqdm(total=len(train_dataloader), disable=not accelerator.is_local_main_process)
        progress_bar.set_description(f"Epoch {epoch}")

        for step, batch in enumerate(train_dataloader):
            clean_images = batch['images']
            # Sample noise to add to the images
            noise = torch.randn(clean_images.shape).to(clean_images.device)
            bs = clean_images.shape[0]

            # Sample a random timestep for each image
            timesteps = torch.randint(0, config.noise_scheduler.num_train_timesteps, (bs,), device=clean_images.device).long()

            # Add noise to the clean images according to the noise magnitude at each timestep
            # (this is the forward diffusion process)
            noisy_images = config.noise_scheduler.add_noise(clean_images, noise, timesteps)
            
            with accelerator.accumulate(model):
                # Predict the noise residual
                preds = model(noisy_images, timesteps)
                # print(preds["sample"], len(preds.sample))
                if hasattr(preds, "sample"):
                    try: 
                        noise_pred = preds["sample"]
                        loss = F.mse_loss(noise_pred, noise)
                        accelerator.backward(loss)

                        accelerator.clip_grad_norm_(model.parameters(), 1.0)
                        optimizer.step()
                        lr_scheduler.step()
                        optimizer.zero_grad()
                    except KeyError:
                        print(f"skipping got an KeyError for sample in step: {step}")
                else: 
                    print(f"No sample found in step: {step} current batch ... continuing with next epoch")
            
            progress_bar.update(1)
            logs = {"loss": loss.detach().item(), "lr": lr_scheduler.get_last_lr()[0], "step": global_step}
            accelerator.log(logs, step=global_step)
            metrics['train_loss'].append(loss.detach().item())
            progress_bar.set_postfix(**logs)
            accelerator.log(logs, step=global_step)
            global_step += 1

        # After each epoch you optionally sample some demo images with evaluate() and save the model
        if accelerator.is_main_process:
            pipeline = DDPMPipeline(unet=accelerator.unwrap_model(model), scheduler=config.noise_scheduler)

            if (epoch + 1) % config.save_image_epochs == 0 or epoch == config.num_epochs - 1:
                evaluate(config, epoch, pipeline)

            if (epoch + 1) % config.save_model_epochs == 0 or epoch == config.num_epochs - 1:
                if config.push_to_hub:
                    push_to_hub(config, pipeline, repo, commit_message=f"Epoch {epoch}", blocking=True)
                else:
                    pipeline.save_pretrained(config.output_dir) 
        # create a Torch checkpoint from the models state dictionary after each
        # epoch and report the metrics 
        # checkpoint = TorchCheckpoint.from_state_dict(model.module.state_dict())
        checkpoint = TorchCheckpoint.from_state_dict(model.state_dict())
        session.report(metrics, checkpoint=checkpoint)