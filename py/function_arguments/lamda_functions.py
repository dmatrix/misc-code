"""
Lambda functions are anonymous functions that can be both used inline or passed
as functional arguments

Form: lambda parameters: expression, where the expression takes the arguments
evaluates and returns the value of the expression
"""

square = lambda x: x ** 2
mult = lambda x, y: x * y
add = lambda x, y: x + y
div = lambda x, y: x / y
cond = lambda x, y: x if x > y else y

if __name__ == '__main__':
    print(f'lambda: square : {square(2)}')
    print(f'lambda: mult : {mult(2, 3)}')
    print(f'lambda: add : {add(2, 3)}')
    print(f'lambda: div: {div(6, 3)}')
    print(f'lambda: cond: {cond(6, 3)}')
