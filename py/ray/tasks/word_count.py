import ray

# Initialize Ray
ray.init()

@ray.remote
def count_words(text):
    """Count the number of words in a given text.

    Args:
        text (str): Text to count the words in.

    Returns:
        int: Number of words in the text.
    """
    words = text.split()
    return len(words)

def word_count_parallel(texts):
    """Perform word count in parallel using Ray.

    Args:
        texts (list): List of texts to count the words in.

    Returns:
        list: List of word counts for each text.
    """
    results = []
    word_counters = [count_words.remote(text) for text in texts]
    results = ray.get(word_counters)
    return results

# Example usage:
text_list = [
    "Hello world",
    "This is a sentence",
    "Python is awesome"
]

counts = word_count_parallel(text_list)
print(counts)

# Shutdown Ray
ray.shutdown()
