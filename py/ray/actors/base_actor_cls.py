from typing import Dict, Any
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split

# states to inspect 
STATES = ["INITIALIZED", "RUNNING", "DONE"]

class ActorCls:
    """
    Base class for our model Actor workers
    """
    def __init__(self, configs: Dict[Any, Any]) -> None:
        self.configs = configs
        self.name = configs["name"]
        self.state = STATES[0]
        self.X, self.y = None, None
        self.X_train, self.X_test = None, None
        self.y_train, self.y_test = None, None
        self.model = None

    def get_name(self) -> str:
        return self.name

    def get_state(self) -> str:
        return self.state
    

    def _prepare_data_and_model(self) -> None:
        self.X, self.y = fetch_california_housing(return_X_y=True, as_frame=True)
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.2, random_state=4)

    def train_and_evaluate_model(self) -> Dict[Any, Any]:
        """
        Super class overwrites this training function
        based its respective ML algorithm
        """
        pass