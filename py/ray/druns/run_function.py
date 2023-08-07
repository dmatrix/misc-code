import argparse
import subprocess

def run(cmd: str):
    subprocess.run(cmd, shell=True, check=True)

def run_on_every_node(remote_func_or_actor_class, *remote_args, **remote_kwargs):
    refs = []
    print("run on everynode...")
    run(remote_func_or_actor_class)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("function", type=str, help="function in this file to run")
    parser.add_argument("args", nargs="*", type=str, help="string args to function")
    args = parser.parse_args()


    if args.function not in globals():
        raise ValueError(f"{args.function} doesn't exist")
    fn = globals()[args.function]
    assert callable(fn) or hasattr(fn, "_function")
    print(f"Running {args.function}({', '.join(args.args)})")
    if hasattr(fn, "_function"):
        run_on_every_node(fn, *args.args)
    else:
        fn(*args.args)