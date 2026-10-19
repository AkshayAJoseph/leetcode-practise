class Solution:
    def fizzBuzz(self, n: int) -> List[str]:
        res = []
        i, fizz, buzz = 1, 0, 0

        while i <= n:
            fizz += 1
            buzz += 1

            if fizz == 3 and buzz == 5:
                res.append("FizzBuzz")
                fizz = buzz = 0
            elif fizz == 3:
                res.append("Fizz")
                fizz = 0
            elif buzz == 5:
                res.append("Buzz")
                buzz = 0
            else:
                res.append(str(i))

            i += 1

        return res