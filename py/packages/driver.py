import parent as p
import parent.one.one_a as o
import parent.two.two_b as t

if __name__ == '__main__':
    print(f"REPO_DIR_NAME_VALUE:{p.REPO_DIR_NAME}")
    print(f"DEFAULT_CLUSTER_VALUE:{p.DEFAULT_CLUSTER}")
    print("--" * 14)
    print(f"REPO_DIR_NAME_PATH:{p.get_repo_dir()}")
    print(f"DEFAULT_CLUSTER_PATH:{p.get_cluster()}")
    print("--" * 17)
    print(o.one_a_func())
    print(t.two_b_func())

