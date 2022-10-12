from distutils.log import warn
import warnings
import ray

from ray import serve
from ray.serve import PredictorDeployment
from ray.data.datasource import SimpleTorchDatasource
import air_utils as aut

from ray.train.torch import TorchTrainer
from ray.tune import Tuner
from ray.tune import TuneConfig
from ray.air.config import RunConfig
from ray.air.config import ScalingConfig
from ray.air.config import CheckpointConfig

from ray.train.torch import TorchPredictor
from ray.train.batch_predictor import BatchPredictor

import numpy as np
import requests
import torch


my_runtime_env = {"pip": ["ray[serve]"],      # Python packages dependencies
                  "working_dir": ".", "excludes":[ "datasets", "images"] # local directory uploaded and accessble to Ray tasks
}

if __name__ == "__main__":

    warnings.filterwarnings('ignore')
    if ray.is_initialized():
        ray.shutdown()
    ray.init(runtime_env=my_runtime_env)

    # Step 1: Fetch data and preprocess for data preparation
    train_dataset: ray.data.Dataset = ray.data.read_datasource(SimpleTorchDatasource(), parallelism=1, dataset_factory=aut.train_dataset_factory)
    test_dataset: ray.data.Dataset = ray.data.read_datasource(SimpleTorchDatasource(), parallelism=1, dataset_factory=aut.test_dataset_factory)
   
    # Transform data into Pandas DataFrame
    # convert training and testing datasets into Panda DataFrame
    # Use dataset map_batches to convert 
    train_dataset = train_dataset.map_batches(aut.convert_batch_to_pandas)
    test_dataset = test_dataset.map_batches(aut.convert_batch_to_pandas)

    print(f"train_dataset={train_dataset}")
    print(f"test_dataset={train_dataset}")
   
    # Step 2: Create a trainer for PyTorch DDP training
    trainer = TorchTrainer(
        train_loop_per_worker=aut.train_loop_per_worker,
        datasets={"train": train_dataset},
        scaling_config=ScalingConfig(num_workers=2), 
    )
    # Step 3: Create the Tuner and the relevant tune configuration
    # such as lr, batch_size, epochs. 
    # 
    tuner = Tuner(trainer,
        param_space={
            "train_loop_config": {
                "lr": ray.tune.grid_search([0.001]),
                "batch_size": ray.tune.grid_search([16, 32]),
                "epochs": ray.tune.grid_search([75, 100]),
            }
        },
        # specific tune metrics to collect and checkpoint
        # during trials
        tune_config=TuneConfig(metric="train_loss", mode="min"),
        run_config=RunConfig(checkpoint_config=CheckpointConfig(num_to_keep=1, 
                        checkpoint_score_attribute="train_loss", 
                        checkpoint_score_order="min")
        )
    )

    # Run the tuner, which will call trainer for each trial with
    # the parameters configurations as part of it HPO
    results = tuner.fit()

    # Get the best checkpoint result
    best_checkpoint = results.get_best_result(metric="train_loss", mode="min").checkpoint

    # Step 4: Do batch inference at scale
    # Test our model with TorchPredictor using the Checkpoint object.
    # Fetch the best_checkpoint from the lastest checkpoint. 
    # Use batch predictor to test the entire batch in one go
    predict_dataset = test_dataset.drop_columns(cols=["label"])
    batch_predictor = BatchPredictor.from_checkpoint(
        checkpoint=best_checkpoint,
        predictor_cls=TorchPredictor,
        model=aut.Net()
    )
    output: ray.data.Dataset = batch_predictor.predict(
        data=test_dataset, dtype=torch.float, 
        feature_columns=["image"], 
        keep_columns=["label"]
    )
    # get the predictions
    predictions = output.map_batches(aut.convert_logits_to_classes, batch_format="pandas")

    # Get all predictions for test_dataset 
    scores = predictions.map_batches(aut.calculate_prediction_scores)

    # compute total prediction accuracy. That is all predictions equal to ground truth,
    # predicted correctly.
    total_acc = scores.sum(on="correct") / scores.count()
    print(f"Prediction accuracy from the test data of 10,000 images: {total_acc:.2f}")

    # Step 5: Do Online prediction
    # Deploy to the network for online prediction
    serve.start(detached=True)
    deployment = PredictorDeployment.options(name="cifar-10-deployment")
    deployment.deploy(TorchPredictor, best_checkpoint, batching_params=False, model=aut.Net(), 
                            http_adapter=aut.json_to_numpy)

    # Test online deployment
    batch = test_dataset.take(10)
    for i in range(10):
        array = np.expand_dims(np.array(batch[i]["image"]), axis=0)
        label = np.array(batch[i]["label"])

        # Send request and fetch prediction
        payload  = {"array": array.tolist()}
        response = requests.post(deployment.url, json=payload)
        result = response.json()[0]
        idx, cls = aut.to_prediction_cls(result)
        matched = idx == label
        aut.img_show(batch[i]["image"])
        print(f"prediction: {idx}; class: {cls}; matched: {matched}")
    serve.shutdown()

