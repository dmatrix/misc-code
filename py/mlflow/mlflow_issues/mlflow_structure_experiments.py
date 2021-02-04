import mlflow

EXPERIMENT_FOLDERS = ["project-1", "project-2", "project-3", "project-4"]

if __name__ == '__main__':

    for experiment in EXPERIMENT_FOLDERS:
        folder = f"MyExperiments/{experiment}"
        mlflow.set_experiment(folder)
        exp = mlflow.get_experiment_by_name(folder)

        with mlflow.start_run(experiment_id=exp.experiment_id):
            mlflow.log_param("project_experiment", folder)

    # Log runs under a particular experiment folder/project
    exp = mlflow.get_experiment_by_name("MyExperiments/project-1")
    for i in range(10):
       with mlflow.start_run(experiment_id=exp.experiment_id):
            mlflow.log_metric("metric-" + str(i), i)
