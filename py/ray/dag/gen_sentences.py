import random

# Predefined lists of words
subjects = ["The cat", "A dog", "John", "Mary", "A homeless personclear", "A lion", "Jules"]
verbs = ["walks", "runs", "jumps", "drives", "sleeps, eats", "codes"]
objects = ["home", "to the park", "at the store", "in the garden", "on the road", "at the office", "in the kitchen"]

def generate_random_sentence():
    # Construct a sentence by randomly choosing a subject, verb, and object
    return f"{random.choice(subjects)} {random.choice(verbs)} {random.choice(objects)}."

def generate_n_random_sentences(n):
    # Generate 'n' random sentences
    return [generate_random_sentence() for _ in range(n)]

# Example: Generate 5 random sentences
N = 10
random_sentences = generate_n_random_sentences(N)

if __name__ == "__main__":
    for sentence in random_sentences:
        print(sentence)
