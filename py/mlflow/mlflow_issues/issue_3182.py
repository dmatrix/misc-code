import os

from pysftp.helpers import known_hosts
from paramiko.hostkeys import HostKeys

if __name__ == '__main__':
    h = HostKeys()

    try:
        kh = known_hosts()
        print("known_hosts:", kh)
        h.load(os.path.expanduser(kh))
    except Exception as e:
        print(e)

    print(len(h.items()))
