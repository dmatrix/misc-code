#
# Code snippet for https://mlflow.org/docs/latest/python_api/mlflow.html#create_experement
#
import warnings
import mlflow

if __name__ == "__main__":

    warnings.filterwarnings("ignore")
    print(mlflow.__version__)

    def print_experiement_info(experiment):
        print("Name:{}".format(experiment.name))
        print("Experiment_id:{}".format(experiment.experiment_id))
        print("Lifecycle_stage:{}".format(experiment.lifecycle_stage))

    # Create experiments. Use names which are unique and case sensitive
    for e in ["E", "e"]:
        experiment_id = mlflow.create_experiment(e)
        experiment = mlflow.get_experiment(experiment_id)
        print_experiement_info(experiment)
