from typing import Tuple
from random import randint

"""Some simple excercises for string manipulation
"""

def reverse_string(s: str) -> str:
    """Reverse a string."""
    return s[::-1]

def is_palinrome(s: str) -> bool:
    """Check if a string is a palindrome."""
    return s == reverse_string(s)

def is_substring(s: str, sub: str) -> bool:
    """Check if a string is a substring of another string."""
    return sub in s

def string_occurrences(s: str, sub: str) -> int:
    """Count the occurrences of a substring in a string."""
    return s.count(sub)

def compute_occurances_of_each_letter(s: str) -> dict:
    """Count the occurrences of each letter in a string."""
    return {letter: s.count(letter) for letter in s}

def palindromes_with_a_substring(s: str, sub: str) -> list:
    """Return all the palindromes that contain a substring."""
    return [s[i:j] for i in range(len(s)) 
            for j in range(i + 1, len(s) + 1) if is_palinrome(s[i:j]) and sub in s[i:j]]

if __name__ == "__main__":
    # Test all above functions  
    print(reverse_string("hello"))
    print(is_palinrome("hello"))
    print(is_substring("hello", "ell"))
    print(string_occurrences("hello", "l"))
    print(compute_occurances_of_each_letter("hello"))
    print(palindromes_with_a_substring("hellolle", "ell"))

# The above code is a simple excercise for string manipulation

