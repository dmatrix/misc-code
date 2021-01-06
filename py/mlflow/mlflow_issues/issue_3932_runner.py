import mlflow


def print_run_infos(run_infos):
    for r in run_infos:
        print("- run_id: {}, status: {}, lifecycle_stage: {}".format(r.run_id, r.status, r.lifecycle_stage))


if __name__ == '__main__':

   exp = mlflow.get_experiment_by_name("issue_3932")
   if exp:
       print_run_infos(mlflow.list_run_infos(experiment_id=exp.experiment_id))
   else:
       print("Experiment name: {} doesn't exist".format("issue_3932"))
