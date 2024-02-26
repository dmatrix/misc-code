def solution(inputArray):
    a = 0
    for i in range(1, len(inputArray)):
        if inputArray[i] <= inputArray[i - 1]:
            f = (inputArray[i - 1] - inputArray[i]) + 1
            inputArray[i] = inputArray[i - 1] + 1
            a += f
    return a

def pyramid(n):
    for i in range(n):
        print(' ' * (n - i - 1) + '*' * (2 * i + 1))
if __name__ == "__main__":
    print(solution([2, 1, 10, 1]))
    pyramid(0)
    for i in range(5):
        print(f"--- n={i+1}  --")
        pyramid(i + 1)
        

