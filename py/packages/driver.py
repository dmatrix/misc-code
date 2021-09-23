import parent
import parent.one.one_a as ONE
import parent.two.two_b as TWO

if __name__ == '__main__':
    print(f"REPO_DIR_NAME:{parent.REPO_DIR_NAME}")
    print(f"DEFAULT_CLUSTER:{parent.DEFAULT_CLUSTER}")
    print("--" * 10)
    print(f"REPO_DIR_NAME:{parent.get_repo_dir()}")
    print(f"DEFAULT_CLUSTER:{parent.get_cluster()}")
    print("--" * 10)
    print(ONE.one_a_func())
    print(TWO.two_b_func())
