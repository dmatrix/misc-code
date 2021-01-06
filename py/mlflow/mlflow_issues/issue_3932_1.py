import mlflow


def print_run_infos(r):
    print("- run_id: {}, status: {}, lifecycle_stage: {}".format(r.run_id, r.status, r.lifecycle_stage))


def get_experiment_id(name='issue_3932'):
    exp = mlflow.get_experiment_by_name(name)
    if exp:
        return exp.experiment_id
    return mlflow.create_experiment(name)


if __name__ == '__main__':
    exp_id = get_experiment_id()
    run = mlflow.start_run(experiment_id=exp_id)
    mlflow.log_metric('m', 3932)
    mlflow.set_tag('issue_3932', 'test')
    print_run_infos(run.info)
    exit()
    mlflow.end_run()
