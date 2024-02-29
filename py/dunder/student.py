from typing import Any


class Student:
    """A simple class to represent a student and add dunder methods to it."""
    def __init__(self, name:str, age:int, grade:str, course:str) -> None:
        self.name = name
        self.age = age
        self.course = course
        self.grade = grade

    def __str__(self) -> str:
        return f"{self.name} is {self.age} years old and is studying {self.course} and recevied a grade of {self.grade}"
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.name}, {self.age}, {self.grade}, {self.course})"
    
    def __eq__(self, __value: object) -> bool:
        return self.__dict__ == __value.__dict__
    
    def __gt__(self, __value: object) -> bool:
        return self.grade > __value.grade and self.course == __value.course
    
    def __lt__(self, __value: object) -> bool:
        return self.grade < __value.grade and self.course == __value.course
    
    def __ge__(self, __value: object) -> bool:
        return self.grade >= __value.grade and self.course == __value.course
    
    def __le__(self, __value: object) -> bool:
        return self.grade <= __value.grade and self.course == __value.course
    
    def __ne__(self, __value: object) -> bool:
        return self.grade != __value.grade and self.course == __value.course
    
    def __hash__(self) -> int:
        return hash(self.__dict__)
    
    def dict(self) -> dict:
        return self.__dict__

if __name__ == "__main__":
    # Generate 10 random students

    from random import randint, choice
    from string import ascii_letters

    # Use facker to generate random names
    from faker import Faker
    fake = Faker()

    # Generate 10 random students
    students = [Student(
        fake.name(),
        randint(18, 25),
        choice(["A", "B", "C", "D", "F"]),
        choice(["Math", "Science", "History", "English"])
    ) for _ in range(10)]

    print(students)

    # Test the dunder methods
    print(students[0] == students[1])
    print(students[0] > students[1])
    print(students[0] < students[1])
    print(students[0] >= students[1])
    print(students[0] <= students[1])

    # Test the __str__ and __repr__ methods
    print(students[0])

    # Sort the students by grade
    print("-- sorted by grade --")
    sorted_students = sorted(students, key=lambda x: x.grade)
    print(sorted_students)

    print("-- sorted by course --")
    # sort the students by course
    sorted_students = sorted(students, key=lambda x: x.course)
    print(sorted_students)

    print("-- sorted by age --")
    # sort the students by age
    sorted_students = sorted(students, key=lambda x: x.age)
    print(sorted_students)

    # sort by grade and course
    print("-- sorted by grade and course --")
    sorted_students = sorted(students, key=lambda x: (x.grade, x.course))
    print(sorted_students)

    # filter out only the students who received an A
    print("-- students who received an A --")
    filtered_students = list(filter(lambda x: x.grade == "A", students))
    print(filtered_students)

    # filter out only the students who received an A in Math
    print("-- students who received an A in Math --")
    filtered_students = list(filter(lambda x: x.grade == "A" and x.course == "Math", students))
    print(filtered_students)

    # filter out only the students who received an A in English or Math
    print("-- students who received an A in English or Math --")
    filtered_students = [x for x in students if x.grade == "A" and (x.course == "Math" or x.course == "English")]   
    print(filtered_students)

    print("--dict--")
    print(students[1].__dict__)
    print(students[1].dict())
    print(students[1].__dict__ == students[1].dict())

