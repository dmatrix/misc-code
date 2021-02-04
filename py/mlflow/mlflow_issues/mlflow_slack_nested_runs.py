import mlflow

if __name__ == '__main__':
    mlflow.set_experiment("Nested Runs")
    exp = mlflow.get_experiment_by_name("Nested Runs")
    # Create nested runs
    with mlflow.start_run(experiment_id=exp.experiment_id, run_name='PARENT_RUN') as parent_run:
        mlflow.log_param("parent", "yes")
        with mlflow.start_run(experiment_id=exp.experiment_id, run_name='CHILD_RUN1', nested=True) as child_run:
            mlflow.log_param("child1", "yes")
            with mlflow.start_run(experiment_id=exp.experiment_id, run_name='CHILD_RUN2', nested=True) as child_run2:
                mlflow.log_param("child2", "yes")
                with mlflow.start_run(experiment_id=exp.experiment_id, run_name='CHILD_RUN3', nested=True) as child_run3:
                    mlflow.log_param("child3", "yes")

# Search all child runs with a parent id
query = "tags.mlflow.parentRunId = '{}'".format(parent_run.info.run_id)
results = mlflow.search_runs(filter_string=query)
print(results)
print(results[["run_id", "params.child", "tags.mlflow.runName"]])
