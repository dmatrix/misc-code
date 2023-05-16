import os
import collections
import ray

ray.init()

@ray.remote
class FileReader:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_file(self):
        with open(self.file_path, "r") as f:
            return f.read()

@ray.remote
def count_words(text):
    words = text.split()
    return collections.Counter(words)

# Define the mapper function to read a file and count its words
def map_fn(file_path):
    file_reader = FileReader.remote(file_path)
    text = ray.get(file_reader.read_file.remote())
    return ray.get(count_words.remote(text))

# Define the reducer function to merge the word counts from multiple files
def reduce_fn(word_counts1, word_counts2):
    return word_counts1 + word_counts2

# Get the list of files to process
file_paths = [os.path.join("data", f) for f in os.listdir("data")]

# Perform the map-reduce operation to count the words in all files
word_counts = ray.util.iter.from_sequence(file_paths).map(map_fn).reduce(reduce_fn)

# Print the total word count
print("Total word count:", sum(word_counts.values()))

# Print the count of each word
for word, count in word_counts.items():
    print(f"{word}: {count}")
