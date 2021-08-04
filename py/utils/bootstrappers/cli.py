from importlib.abc import Loader


def init_config():
    import importlib.util
    from pathlib import Path
    import os
    # get current working directory and set the config path
    config_path = Path(os.getcwd())
    bootstrap_path = config_path / "bootstrap.py"

    # import file location and module
    spec = importlib.util.spec_from_file_location("bootstrap", str(bootstrap_path))
    bootstrap = importlib.util.module_from_spec(spec)
    assert isinstance(spec.loader, Loader)

    # execute the function bootstrap() in the loaded file
    spec.loader.exec_module(bootstrap)
    bootstrap.bootstrap()


if __name__ == '__main__':
    init_config()