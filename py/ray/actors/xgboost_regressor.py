
import xgboost as xgb
import time
from typing import Dict, Any
from base_actor_cls import ActorCls, STATES
from sklearn.metrics import mean_squared_error
from pprint import pprint
import ray


@ray.remote
class XGBoostActor(ActorCls):
    def __init__(self, configs):
        super().__init__(configs)
        self.max_depth = configs["max_depth"]
        self.estimators = configs["n_estimators"]
        self.colsample = configs["colsample_bytree"]
        self.eta = configs["eta"]
        self.lr = configs["lr"]
    
    def train_and_evaluate_model(self) -> Dict[Any, Any]:

        self._prepare_data_and_model()
        self.model = xgb.XGBRegressor(objective='reg:squarederror',
                                      colsample_bytree=self.colsample,
                                      eta=self.eta,
                                      learning_rate = self.lr,
                                      max_depth=self.max_depth,
                                      n_estimators=self.estimators,
                                      random_state=42)

        print(f"Start training model {self.name} with estimators: {self.estimators} and max depth: { self.max_depth } ...")
        start_time = time.time()
        self.model.fit(self.X_train, self.y_train)
        self.state = STATES[1]
        y_pred = self.model.predict(self.X_test)
        score = mean_squared_error(self.y_test, y_pred)
        self.state = STATES[2]

        end_time = time.time()
        print(f"End training model {self.name} with estimators: {self.estimators} and max depth: { self.max_depth } and took: {end_time - start_time:.2f}")

        return {"state": self.get_state(), 
                "name": self.get_name(),
                "max_depth": self.max_depth, 
                "mse": round(score, 4), 
                "estimators": self.estimators,
                "time": round(end_time - start_time, 2)}

if __name__ == "__main__":
    configs = {"max_depth": 10,
               "n_estimators": 150,
               "lr": 0.1,
               "eta": 0.3,
               "colsample_bytree": 1,
               "name": "xgboost"}
    model_cls = XGBoostActor.remote(configs)
    values = ray.get(model_cls.train_and_evaluate_model.remote())
    pprint(values)
    


