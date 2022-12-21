import ray
from random_forest_regressor import RFRActor
from decsion_tree import DTActor
from xgboost_regressor import XGBoostActor

DECISION_TREE_CONFIGS = {"max_depth": 15,
                         "name": "decision_tree"}

RANDOM_FOREST_CONFIGS = {"n_estimators": 150,
                        "name": "random_forest"}

XGBOOST_CONFIGS = {"max_depth": 10,
                   "n_estimators": 150,
                   "lr": 0.1,
                   "eta": 0.3,
                   "colsample_bytree": 1,
                   "name": "xgboost"}

class ModelFactory:
    MODEL_TYPES = ["random_forest", "decision_tree", "xgboost"]
    
    @staticmethod
    def create_model(model_name: str) -> ray.actor.ActorHandle:
        if model_name not in ModelFactory.MODEL_TYPES:
            raise Exception(f"{model_name} not supported")
        if model_name == "random_forest":
             configs = RANDOM_FOREST_CONFIGS
             return RFRActor.remote(configs)
        elif model_name == "decision_tree":
            configs = DECISION_TREE_CONFIGS
            return DTActor.remote(configs)
        else: 
            configs = XGBOOST_CONFIGS
            return XGBoostActor.remote(configs)

@ray.remote
class Supervisor:
    def __init__(self):
        # Create three Actor Workers, each by its unique model type and 
        # their respective training function
        self.worker_models =  [ModelFactory.create_model(name) for name in ModelFactory.MODEL_TYPES]

    def work(self):
        # do the work 
        results = [worker_model.train_and_evaluate_model.remote() for worker_model in self.worker_models]
        return ray.get(results)

if __name__ == "__main__":
    supervisor = Supervisor.remote()
    results = supervisor.work.remote()
    values = ray.get(results)
    states = []

    # Wait for all models to finish
    while True:
        for value in values:
            states.append(value[0])
        result = all('DONE' == e for e in states)
        if result:
            break

    print(f"\n Results from three training models: {values}")



