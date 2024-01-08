import os
from pathlib import Path

# Get the current working directory
cwd = os.getcwd()
print(f"Current working dir: {cwd}")

# Get the current working file
file_path = Path(__file__).resolve()
print(f"Curent working file: {file_path}")

# Get the parent directory of the current working file
file_dir = file_path.parent
print(f"Current working dir's parent: {file_dir}")

# check if the is a file or directory
print(f"Is '{file_path}' a directory? :{file_path.is_dir()}")
print(f"Is '{file_dir}' a directory? :{file_dir.is_dir()}")

# join the file_dir with test.txt
new_file = Path.joinpath(file_dir, "test.txt")
print(f"New file: {new_file}")
with open(new_file, "w") as f:
    f.write("Hello World!")

# reading contents of a file
print(f"Contents of file:{new_file}")
with open(new_file, "r") as f:
    print(f.read())

# Listing all files in a directory
print("Files in directory:")
for file in file_dir.iterdir():
    if file.is_file():
        print(file)
