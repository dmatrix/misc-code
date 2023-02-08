
from dataclasses import dataclass
from typing import Dict, Tuple, List, Any
import datasets as hf
from ray.train.huggingface import HuggingFaceTrainer
from transformers import TrainingArguments, Trainer
from ray.air.config import RunConfig
from ray.air.config import ScalingConfig
from torchvision import transforms
from ray.air import session
import ray

BUTTER_FLY_DATASET = "huggan/smithsonian_butterflies_subset"     # 1K rows
# BUTTER_FLY_DATASET  = "ceyda/smithsonian_butterflies"          # 9K rows

@dataclass
class TrainingConfig:
    image_size = 128  # the generated image resolution
    train_batch_size = 16
    eval_batch_size = 16  # how many images to sample during evaluation
    num_epochs = 50
    gradient_accumulation_steps = 1
    learning_rate = 1e-4
    lr_warmup_steps = 500
    save_image_epochs = 10
    save_model_epochs = 30
    mixed_precision = 'fp16'  # `no` for float32, `fp16` for automatic mixed precision
    output_dir = 'ddpm-butterflies'  # the model namy locally and on the HF Hub
    num_workers = 4,
    push_to_hub = True  # whether to upload the saved model to the HF Hub
    hub_private_repo = False  
    overwrite_output_dir = True  # overwrite the old model when re-running the notebook
    dataset = BUTTER_FLY_DATASET
    seed = 0

tr_config = TrainingConfig()

def trainer_init_per_worker(train_dataset, eval_dataset=None, **config) -> None:

    epochs = config.get("epochs", 5)
    batch_size = config.get("batch_size", 16)

    args = TrainingArguments("ddpm-butterflies",
        evaluation_strategy="epoch",
        save_strategy="epoch",
        logging_strategy="epoch",
        learning_rate=config.get("learning_rate", 2e-5),
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        num_train_epochs=epochs,
        weight_decay=config.get("weight_decay", 0.01),
        push_to_hub=False,
        disable_tqdm=True,  # declutter the output a little
        no_cuda=False,  # you need to explicitly set no_cuda if you want CPUs
    )

    trainer = Trainer(
        None,
        args,
        train_dataset=train_dataset,
    )
    print("Starting training")
    return trainer

preprocess = transforms.Compose(
        [
            transforms.Resize((tr_config.image_size, tr_config.image_size)),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            transforms.Normalize([0.5], [0.5]),
        ]
    )

def transform(examples):
    images = [preprocess(image.convert("RGB")) for image in examples["image"]]
    return {"images": images}

if __name__ == "__main__":
    hf_datasets = hf.load_dataset(tr_config.dataset, split="train")
    
    # Do some transformations
    hf_datasets.set_transform(transform)

    # Convert HF dataset to Ray data
    ray_datasets = ray.data.from_huggingface(hf_datasets["image"])

    trainer = HuggingFaceTrainer(trainer_init_per_worker=trainer_init_per_worker,
                                scaling_config=ScalingConfig(num_workers=4, use_gpu=False),
                                datasets={"train": ray_datasets})
    result = trainer.fit()

    
