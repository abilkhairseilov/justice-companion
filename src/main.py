class AIHelper:
    def fib(self, n: int) -> int:
        '''
        Calculate the nth Fibonacci number.
        `n`: `int` - The position in the Fibonacci sequence.
        '''
        if n == 1:
            return 1
        if n == 0:
            return 0
        res: int = AIHelper.fib(self, n-1) + AIHelper.fib(self, n-2)
        return res

if __name__ == "__main__":
    print("Hello World!")

AI = AIHelper()
print(AI.fib(10))
