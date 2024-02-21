from typing import Tuple
from random import randint

# Some simple excercises for list manipulation

def find_smallest_number_index(lst) -> Tuple[int, int]:
    """Find the index of the smallest number in the list and the number."""
    small_idx = 0
    # set the first number as the smallest number
    small_num = lst[0]
    # iterate through the list
    for idx in range(len(lst)):
        # if the number in the list is smaller than the current smallest number
        if small_num > lst[idx]:
            small_idx = idx
            small_num = lst[idx]
    return (small_idx, small_num)
        

def find_largest_number_index(lst) -> Tuple[int, int]:
    """
    Find the index of the largest number in the list and the number.
    """
    large_idx = 0
    # set the first number as the largest number
    large_num = lst[0]
    # iterate through the list
    for idx in range(len(lst)):
        # if number in the list is larger than the current largest number
        if large_num < lst[idx]:
            large_idx = idx
            large_num = lst[idx]
    return (large_idx, large_num)

def compute_average_and_sum(lst) -> Tuple[float, int]:
    """
    Compute the average and sum of the list.
    """
    sum = 0
    for num in lst:
        sum += num
    
    return round(sum/len(lst),2), sum

def is_prime(n: int) -> bool:
    """Check if a number is a prime number."""
    if n < 2:
        # 0 and 1 are not prime numbers
        return False
    # iterate through the numbers from 2 to n for divisibility or factors
    for i in range(2, n):
        # if the modulus is 0, then it is not a prime number since it has a factor
        if n % i == 0:
            return False
    return True

def find_factors(n: int) -> list:
    """Find the factors of a number."""
    factors = []
    for i in range(1, n + 1):
        if n % i == 0:
            factors.append(i)
    return factors

def find_even_numbers(lst) -> list:
    """
    Find the even numbers in the list.
    """
    even_lst = []
    for num in lst:
        if is_prime(num):
            even_lst.append(num)
    return even_lst

def find_odd_numbers(lst) -> list:
    """
    Find the odd numbers in the list.
    """
    odd_lst = []
    for num in lst:
        if num %2 != 0:
            odd_lst.append(num)
    return odd_lst  

def find_prime_numbers(lst) -> list:
    """
    Find the prime numbers in the list.
    """
    prime_lst = []
    # iterate through the list
    for num in lst:
        # prime numbers are greater than 1
        if num > 1:
            # check for factors
            for i in range(2, num):
                # if the modulus is 0, then it is not a prime number
                if num % i == 0:
                    break
            else:
                prime_lst.append(num)
    return prime_lst

def count_occurrences(lst, num) -> int:
    """
    Count the occurrences of a number in the list.
    """
    count = 0
    num = lst[0]
    for n in lst:
        if n == num:
            count += 1
    return count

if __name__ == "__main__":
    lst = []
    for _ in range(15):
        lst.append(randint(1, 100))
    print( "--" * 10) 
    print(f"original list         : {lst}")
    print(f"index, smallest number: {find_smallest_number_index(lst)}")
    print(f"index, largest number : {find_largest_number_index(lst)}")
    print(f"avg and sum           : {compute_average_and_sum(lst)}")
    print(f"even numbers          : {find_even_numbers(lst)}")
    print(f"odd numbers           : {find_odd_numbers(lst)}")
    print(f"prime numbers         : {find_prime_numbers(lst)}")  
    print(f"occurrence of {lst[2]}: {count_occurrences(lst, {lst[2]})}")
    print(f"factors of {lst[2]}   : {find_factors(lst[2])}")
    print( "--" * 10) 