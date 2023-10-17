import ray

class DataLoader():
    def __init__(self, val):
        self.attribute = val

class ModelLoader():
    def __init__(self, path):
        self.attribute = path

class Trainer():
    def __init__(self, **kwargs):
        self.attribute = kwargs

    def train(self):
        self.attribute["status"] = "RUNNING"

    def stop(self, status="TERMINATED"):
        self.attribute["status"] = status
       
    def update_trainer_state(self, flag):
        self.attribute["status"] = flag



@ray.remote
class Actor:
    def __init__(self, dloader, mloader, trainer):
        self.dloader = dloader
        self.trainer = trainer
        self.mloader = mloader

    def update_trainer(self, status):
        self.trainer.update_trainer_state(status)

    def get_attributes(self):
        results = {"trainer": self.trainer.attribute,
                   "loader":  self.dloader.attribute,
                   "mloader": self.mloader.attribute     
        }
                   
        return results

if __name__ == "__main__":
    model_cls = ModelLoader("/model/v1")
    data_cls  = DataLoader("pytorch")
    train_cls = Trainer(status="START")
    actor = Actor.remote(data_cls, model_cls, train_cls)

    results = ray.get(actor.get_attributes.remote())
    print(results)

    # change status 
    actor.update_trainer.remote("DONE")

    results = ray.get(actor.get_attributes.remote())
    print(results)
    