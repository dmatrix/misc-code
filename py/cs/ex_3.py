"""
Python data structures examples
"""

# Stack
from typing import Any


class Stack:
    def __init__(self):
        # implement stack using list, last in first out (LIFO)
        self.items = []

    def is_empty(self):
        return self.items == []
    
    def push(self, item) -> None:
        # add item to the top of the stack
        self.items.append(item)
    
    def pop(self) -> object:
        # remove the top item from the stack
        return self.items.pop()
    
    def peek(self) -> object:
        # return the top item from the stack without removing it
        return self.items[len(self.items) - 1]
    
    def size(self) -> int:
        # return the size of the stack
        return len(self.items)
    
    def __str__(self) -> str:
        return str(self.items)
    
# Queue
class Queue:
    def __init__(self):
        # implement queue using list, first in first out (FIFO)
        self.items = []

    def is_empty(self):
        return self.items == []
    
    def enqueue(self, item) -> None:
        # add item to the end of the queue
        self.items.insert(0, item)
    
    def dequeue(self) -> object:
        # remove the first item from the queue
        return self.items.pop()
    
    def size(self) -> int:
        # return the size of the queue
        return len(self.items)
    
    def __str__(self) -> str:
        return str(self.items)
    
# Deque
class Deque:
    def __init__(self):
        # implement deque using list
        self.items = []

    def is_empty(self):
        return self.items == []
    
    def add_front(self, item) -> None:
        # add item to the front of the deque
        self.items.append(item)
    
    def add_rear(self, item) -> None:
        # add item to the end of the deque
        self.items.insert(0, item)
    
    def remove_front(self) -> object:
        # remove the first item from the deque
        if self.items:
            return self.items.pop()
        return None
    
    def remove_rear(self) -> object:
        # remove the last item from the deque
        if self.items:
            return self.items.pop(0)
        return None
    
    def size(self) -> int:
        # return the size of the deque
        return len(self.items)
    
    def __str__(self) -> str:
        return str(self.items)  
    
def is_balanced_parenthesis(s: str) -> bool:
    """Check if a string has balanced parenthesis."""
    stack = Stack()
    for char in s:
        if char == "(":
            stack.push(char)
        elif char == ")":
            if stack.is_empty():
                return False
            stack.pop()
    
    return stack.is_empty()

if __name__ == "__main__":
    # Test the stack
    print("--- Stack ---")
    s = Stack()
    print(s.is_empty())
    s.push(4)
    s.push('dog')
    print(s.peek())
    s.push(True)
    print(s.size())
    print(s.is_empty())

    # Test the queue
    print("--- Queue ---")
    q = Queue()
    print(q.is_empty())
    q.enqueue(4)
    q.enqueue('dog')
    print(q.dequeue())
    q.enqueue(True)
    print(q.size())
    print(q.is_empty())

    # Test the deque
    print("--- Deque ---")
    d = Deque()
    print(d.is_empty())
    d.add_rear(4)
    d.add_rear('dog')
    print(d.remove_rear())
    d.add_front(True)
    print(d.size())
    print(d.is_empty())
    print(d.remove_front())
    print(d.is_empty())
    print(d.add_rear(8.4))
    print(d.add_front('cat'))
    print(d.remove_rear())
    print(d.remove_front())
    print(d.size())
    print(d.is_empty())
    print(d.remove_front())
    print(d.is_empty())
    print(d.remove_rear())
    print(d.is_empty())
    print(d.size())

    # Test is_balanced_parenthesis
    print("--- is_balanced_parenthesis ---")
    s = "((()))"
    print(f"'{s}' is balanced: {is_balanced_parenthesis(s)}")
    s = "(()"
    print(f"'{s}' is balanced: {is_balanced_parenthesis(s)}")
    s = ""
    print(f"'{s}' is balanced: {is_balanced_parenthesis(s)}")

    lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print(f"pop: {lst.pop()}")  # pop: 10
    lst.insert(5, 10)
    print(lst)
    print(f"pop: {lst.pop(5)}")  # pop: 10
    print(lst)
    print(f"pop: {lst.pop(0)}")  # pop: 1

