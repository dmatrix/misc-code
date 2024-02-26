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