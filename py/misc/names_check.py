import re
import sys

_PROJECT_NAME_REGEX = re.compile(r"^[a-zA-Z0-9-_][\w\_]{0,255}$")


def is_project_name_valid(pname: str) -> bool:
    if not pname or pname.startswith("_") or not _PROJECT_NAME_REGEX.match(pname) or pname[0].isdigit():
        return False
    return True


if __name__ == '__main__':
    for name in sys.argv[1:]:
        if not is_project_name_valid(name):
            print("name: {} is invalid project name.".format(name))
        else:
            print("name: {} is valid project name!".format(name))
