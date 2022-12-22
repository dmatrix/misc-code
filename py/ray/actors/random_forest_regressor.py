import time
from typing import Dict, Any
from sklearn.ensemble import RandomForestRegressor
from base_actor_cls import ActorCls, STATES
from sklearn.metrics import mean_squared_error
from pprint import pprint
import ray

@ray.remote
class RFRActor(ActorCls):
    def __init__(self, configs):
        super().__init__(configs)
        self.estimators = configs["n_estimators"]

    def train_and_evaluate_model(self) -> Dict[Any, Any]:
        """
        Implement the Random forest regressor with the appropriate
        parameters
        """

        self._prepare_data_and_model()
        self.model = RandomForestRegressor(n_estimators=self.estimators, random_state=42)

        print(f"Start training model {self.name} with estimators: {self.estimators} ...")

        start_time = time.time()
        self.model.fit(self.X_train, self.y_train)
        self.state = STATES[1]
        y_pred = self.model.predict(self.X_test)
        score = mean_squared_error(self.y_test, y_pred)
        self.state = STATES[2]

        end_time = time.time()
        print(f"End training model {self.name} with estimators: {self.estimators} took: {end_time - start_time:.2f} seconds")

        return  { "state": self.get_state(),
                  "name": self.get_name(),
                  "estimators": self.estimators, 
                  "mse": round(score, 4), 
                  "time": round(end_time - start_time, 2)}


if __name__ == "__main__":
    configs = {"n_estimators": 150, "name": "random_forest"}
    model_cls = RFRActor.remote(configs)
    values = ray.get(model_cls.train_and_evaluate_model.remote())
    print("\nThe returned values from the training:")
    pprint(values)