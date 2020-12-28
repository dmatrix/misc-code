import os

from mlflow.exceptions import MlflowException
from six.moves import urllib
from mlflow.store.model_registry.sqlalchemy_store import SqlAlchemyStore


class PluginRegistrySqlAlchemyStore(SqlAlchemyStore):
    def __init__(self, store_uri=None):
        path = urllib.parse.urlparse(store_uri).path if store_uri else None
        db_uri = "sqlite:///" + os.path.join(path, "fp_mlruns.db") if path else None
        self.is_plugin = True
        super(PluginRegistrySqlAlchemyStore, self).__init__(db_uri)


if __name__ == '__main__':
    path = os.path.join(os.getcwd(), "mlruns")
    uri = "file-plugin://" + path
    exit_code = 0
    try:
        ps = PluginRegistrySqlAlchemyStore(store_uri=uri)
    except MlflowException as mlex:
        print(mlex)
        exit_code = 1
    finally:
        uri = "sqlite:///" + path
        print('\nTrying SqlAlchemyStore... :{}'.format(uri))
        sql_ps = SqlAlchemyStore(db_uri=uri)
        print(sql_ps)
    exit(exit_code)

