# some constants and functions under Parent module

REPO_DIR_NAME = "repo_dir"
DEFAULT_CLUSTER = " local"


def get_repo_dir():
    return _get_url_prefix() + REPO_DIR_NAME


def get_cluster():
    return _get_local_prefix() + DEFAULT_CLUSTER


def _get_url_prefix():
    return "s3://"


def _get_local_prefix():
        return "host->"