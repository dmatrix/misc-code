import ray

from ray import serve
from ray.serve import PredictorDeployment
from ray.data.datasource import SimpleTorchDatasource
import air_utils as aut

from ray.train.torch import TorchTrainer
from ray.air.config import ScalingConfig

from ray.train.torch import TorchPredictor
from ray.train.batch_predictor import BatchPredictor

import torch
import numpy as np
import pandas as pd
import requests

if __name__ == "__main__":
    # Fetch data
    train_dataset: ray.data.Dataset = ray.data.read_datasource(SimpleTorchDatasource(), dataset_factory=aut.train_dataset_factory)
    test_dataset: ray.data.Dataset = ray.data.read_datasource(SimpleTorchDatasource(), dataset_factory=aut.test_dataset_factory)
   
    # Transform data into Pandas DataFrame0
    # convert training and testing datasets into Panda DataFrame
    # Use dataset map_batches to convert 
    train_dataset = train_dataset.map_batches(aut.convert_batch_to_pandas)
    test_dataset = test_dataset.map_batches(aut.convert_batch_to_pandas)

    print(train_dataset)
    print(test_dataset)

    # Train the model
    trainer = TorchTrainer(
        train_loop_per_worker=aut.train_loop_per_worker,
        train_loop_config={"batch_size": 4, "epochs": 50}, # try batch_size, epochs =(8, 75), (10, 100)
        datasets={"train": train_dataset},
        scaling_config=ScalingConfig(num_workers=4) # try mulitples of 2, 4, 6, 8
    )
    result = trainer.fit()
    latest_checkpoint = result.checkpoint

    # Test our model with TorchPredictor using the Checkpoint object.
    # Fetch the best_checkpoint from the lastest checkpoint. 
    # Use batch predictor to test the entire batch in one go
    predict_dataset = test_dataset.drop_columns(cols=["label"])
    batch_predictor = BatchPredictor.from_checkpoint(
        checkpoint=latest_checkpoint,
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

    # compute total prediction accuracy. That is all predictions equal to ground truth
    # That is, predictated accurately.
    total_acc = scores.sum(on="correct") / scores.count()
    print(f"Prediction accuracy from the test data of 10,000 images: {total_acc:.2f}")

    # Deploy to the network for online prediction
    serve.start(detached=True)
    deployment = PredictorDeployment.options(name="cifar-deployment")
    deployment.deploy(TorchPredictor, latest_checkpoint, batching_params=False, model=aut.Net(), http_adapter=aut.json_to_numpy)

    # Test online deployment
    batch = test_dataset.take(10)
    for i in range(5):
        array = np.expand_dims(np.array(batch[i]["image"]), axis=0)
        label = np.array(batch[i]["label"])
        # send request and fetch prediction
        payload  = {"array": array.tolist()}
        response = requests.post(deployment.url, json=payload)
        result = response.json()[0]
        idx, cls = aut.to_prediction_cls(result)
        matched = idx == label
        aut.img_show(batch[i]["image"])
        print(f"prediction: {idx}; class: {cls}; matched: {matched}")
    serve.shutdown()

