from mlflow.tracking import MlflowClient
from mlflow.entities import ViewType

if __name__ == "__main__":

    def print_experiment_info(experiments):
        for e in experiments:
            print("- experiment_id: {}, name: {}, lifecycle_stage: {}"
                  .format(e.experiment_id, e.name, e.lifecycle_stage))

    client = MlflowClient()
    for name in ["Experiment 1", "Experiment 2"]:
        exp_id = client.create_experiment(name)

    # Delete the last experiment
    client.delete_experiment(exp_id)

    # Fetch experiments by view type
    print("Active experiments:")
    print_experiment_info(client.list_experiments(view_type=ViewType.ACTIVE_ONLY))
    print("Deleted experiments:")
    print_experiment_info(client.list_experiments(view_type=ViewType.DELETED_ONLY))
    print("All experiments:")
    print_experiment_info(client.list_experiments(view_type=ViewType.ALL))




