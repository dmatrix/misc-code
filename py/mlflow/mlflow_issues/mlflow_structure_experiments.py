import mlflow

EXPERIMENT_FOLDERS = ["project-{}".format(i) for i in range(100)]

if __name__ == '__main__':
    import logging

    logging.basicConfig()
    logging.getLogger('sqlalchemy').setLevel(logging.ERROR)

    mlflow.set_tracking_uri("sqlite:///mlruns.db")
    for experiment in EXPERIMENT_FOLDERS:
        folder = f"MyExperiments/{experiment}"
        mlflow.set_experiment(folder)
        exp = mlflow.get_experiment_by_name(folder)
        for i in range(1000):
            with mlflow.start_run(experiment_id=exp.experiment_id):
                mlflow.log_param("project_experiment", folder)
                mlflow.log_metric("m", i)
