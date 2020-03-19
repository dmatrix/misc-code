#
# An example of user-defined-dictionary that only stores `str` as
# keys. that is given a non-str, it'll convert it not a str

import collections

class StrKeyDict(collections.UserDict):

    def __missing__(self, key):
        if isinstance(key,str):
            raise KeyError(key)
        return self[str(key)]

    def __contains__(self, item):
        return str(key) in self.data

    def __setitem__(self, key, value):
        self.data[key] = value

if __name__ == '__main__':

    usr_dd = StrKeyDict([('2', 'two'), ('4', 'four')])
    # use d[key] notation
    print(usr_dd['2'])
    print(usr_dd['4'])
    try:
        print(usr_dd['5'])
    except KeyError as ex:
        print("KeyError: {}".format(ex))
    # use d.get() notation
    print(usr_dd.get('2'))
    print(usr_dd.get('4'))
    print(usr_dd.get(5))

