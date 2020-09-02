from mlflow.tracking import MlflowClient

class _ActiveRun():  # pylint: disable=W0223
    """Wrapper around :py:class:`mlflow.entities.Run` to enable using Python ``with`` syntax."""

    def __init__(self, run):
        self._run = run

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        status = "FINISHED" if exc_type is None else "FAILED"
        return exc_type is None

def create_run():
    """
    Create a new run and return the run_id
    """
    return MlflowClient.create_run()

def get_run(run_id):
    """
    Fetch the run from backend store. The resulting :py:class:`Run <mlflow.entities.Run>`
    contains a collection of run metadata -- :py:class:`RunInfo <mlflow.entities.RunInfo>`,
    as well as a collection of run parameters, tags, and metrics --
    :py:class:`RunData <mlflow.entities.RunData>`. In the case where multiple metrics with the
    same key are logged for the run, the :py:class:`RunData <mlflow.entities.RunData>` contains
    the most recently logged value at the largest step for each metric.
    :param run_id: Unique identifier for the run.
    :return: A single :py:class:`mlflow.entities.Run` object, if the run exists. Otherwise,
                raises an exception.
    """
    return MlflowClient().get_run(run_id)

