import os

# Get the directory name of the python file name
current_dir = os.path.dirname(os.path.abspath(__file__))
path = os.path.normpath(os.path.join(current_dir, os.pardir, os.pardir))
print(f"os.pardir={os.pardir}")
print(f"current_dir={current_dir}")
print(f"path = {path}")
