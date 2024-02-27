student_tuples = [
    ('john', 'A', 15),
    ('jane', 'B', 12),
    ('dave', 'B', 10),
]

class Student:
    def __init__(self, full_name: str, grade:str, age:int) -> None:
        self.full_name = full_name
        self.grade = grade
        self.age = age

    def __repr__(self) -> str:
        return repr((self.full_name, self.grade, self.age))
    
student_objects = [
    Student(t[0], t[1], t[2]) for t in student_tuples]
        
s = sorted(student_objects, key=lambda student: student.age, reverse=True)   # sort by age
n = sorted(student_objects, key=lambda student: student.full_name)   # sort by name
print(s)
print(n)
print("--" * 10)
# Use itemgetter to sort by multiple keys
from operator import itemgetter
s = sorted(student_tuples, key=itemgetter(2), reverse=True)   # sort by age
print("sorted by age using itemgetter:", s)

# use attrgetter to sort by multiple keys
from operator import attrgetter
s = sorted(student_objects, key=attrgetter('age'), reverse=True)   # sort by age
print("sorted by age using attrgetter:", s)

# The key-function patterns shown above are very common, so Python provides convenience functions to make accessor functions easier and faster. 
# The operator module has itemgetter(), attrgetter(), and methodcaller() functions that create functions key functions for sorting.
# The operator.itemgetter() function takes a list of keys and returns a callable that will fetch the given keys from a record.
# The operator.attrgetter() function takes an attribute name string (or several strings) and returns a callable that fetches the given attribute from its operand.
# The operator.methodcaller() function takes a method name and returns a callable that calls the named method on its operand.

# The operator module functions allow multiple levels of sorting. For example, to sort the student data by grade then by age:
s = sorted(student_objects, key=attrgetter('grade', 'age'))   # sort by grade then by age
print("sorted by grade then by age:", s)
# The operator module functions are useful by themselves, but also as key functions for sort(), min(), max(), itertools.groupby(), and other functions that expect a key function.

from functools import partial
from operator import mul
from unicodedata import normalize

def nfc_equal(str1, str2):
    return normalize('NFC', str1) == normalize('NFC', str2)

s1 = 'café'
s2 = 'cafe\u0301'
print(s1 == s2)

names = 'Zoë Åbjørn Núñez Élana Zeke Abe Nubia Eloise'.split()

print(f"Orignal names: {names}")
print("--sorted: NFD--")
print(sorted(names, key=partial(normalize, 'NFD')))
print("--sorted: NFC--")
print(sorted(names, key=partial(normalize, 'NFC')))

def custom_sort(iterable, key, reverse=False):
    """Customer sort function."""
    # sort by key
    return sorted(iterable, key=key, reverse=reverse)

# Creating a partial function for custom sorting
sort_descending = partial(custom_sort, reverse=True)

numbers = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
numbers_2 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print("--sorted: descending--")
print(f"Original numbers: {numbers}")
print(f"Sorted numbers: {custom_sort(numbers, key=lambda x: x % 3)}")

print("--sorted: descending--")
print(f"Original numbers: {numbers_2}")
print(f"Sorted numbers: {sort_descending(numbers_2, key=lambda x: x % 2)}")

print("--" * 10)

# The functools.partial() function allows one to derive a new function with some of the arguments of the original function fixed.
# This is useful to adapt a function to a specific use case without needing to rewrite the original function.

us_currency = [1, 5, 10, 25, 50, 100]
uk_currency = [1, 2, 5, 10, 20, 50, 100]

# Create a partial function to convert US currency to UK currency
def convert_currency(amount, conversion_rate):
    return amount * conversion_rate

us_to_uk = partial(convert_currency, conversion_rate=0.75)
uk_to_us = partial(convert_currency, conversion_rate=1.33)

print(f"US currency: {us_currency}")
us_2_uk = sorted([us_to_uk(x) for x in us_currency])
print(f"US currency to UK currency: {us_2_uk}")
print("--" * 10)
print(f"UK currency: {uk_currency}")
uk_2_us = sorted([uk_to_us(x) for x in uk_currency])
print(f"UK currency to US currency: {uk_2_us}")


