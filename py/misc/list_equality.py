import os


def listdir(path):
    files = []
    for name in os.listdir(path):
        path_name = os.path.join(path, name)
        if os.path.isdir(path_name):
            listdir(path_name)
        elif os.path.isfile(path_name):
            files.append(name)
        elif os.path.islink(path_name):
            files.append(name)
    return files


def are_dirs_equal(d1, d2, info=True):
    d1_files = os.listdir(dir_1)
    d2_files = os.listdir(dir_2)
    same_len = len(d1_files) == len(d2_files)
    if info:
        print("d1 files: {}".format(d1_files))
        print("d2 files: {}".format(d2_files))
    if not same_len:
        return False
    else:
        return all(file in d1_files for file in d2_files)


if __name__ == '__main__':
    dir_1 = "dir_1"
    dir_2 = "dir_2"

    if are_dirs_equal(dir_1, dir_2):
        print("contents of dir_1 and dir_2 are the same")
    else:
        print("contents of dir_1 and dir_2 are not the same")
    print(listdir(dir_1))
