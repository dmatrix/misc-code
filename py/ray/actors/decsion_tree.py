import time
from typing import Dict, Any
from base_actor_cls import ActorCls, STATES
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error
from pprint import pprint
import ray

@ray.remote
class DTActor(ActorCls):
    def __init__(self, configs):
       super().__init__(configs)
       self.max_depth = configs["max_depth"]

    def train_and_evaluate_model(self) -> Dict[Any, Any]:
        """
        Implement the decision tree regressor with the appropriate
        parameters
        """

        self._prepare_data_and_model()
        self.model = DecisionTreeRegressor(max_depth=self.max_depth, random_state=42)
        print(f"Start training model {self.name} with max depth: { self.max_depth } ...")

        start_time = time.time()
        self.model.fit(self.X_train, self.y_train)
        self.state = STATES[1]
        y_pred = self.model.predict(self.X_test)
        score = mean_squared_error(self.y_test, y_pred)
        self.state = STATES[2]

        end_time = time.time()
        
        print(f"End training model {self.name} with max_depth tree: {self.max_depth} took: {end_time - start_time:.2f} seconds")

        return { "state": self.get_state(), 
                 "name": self.get_name(),
                 "max_depth": self.max_depth, 
                 "mse": round(score, 4), 
                 "time": round(end_time - start_time, 2)}

if __name__ == "__main__":
    configs = {"max_depth": 10, "name": "decision_tree"}
    model_cls = DTActor.remote(configs)
    values = ray.get(model_cls.train_and_evaluate_model.remote())
    pprint(values)
    


