class Solution:
    def isHappy(self, n: int) -> bool:
        def sumsquare(n):
            total = 0 
            while n > 0:
                digit = n % 10
                total += digit * digit
                n //= 10
            return total
        slow = n
        fast = n
        while True:
            slow = sumsquare(slow)
            fast = sumsquare(sumsquare(fast))

            if fast == 1:
                return True
            if slow == fast:
                return False
