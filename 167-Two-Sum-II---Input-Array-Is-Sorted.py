class Solution:
    def twoSum(self, numbers: list[int], target: int) -> list[int]:
        left = 0
        right = len(numbers) - 1
        while left < right:
            c_sum = numbers[left] + numbers[right]
            if c_sum > target:
                right -= 1
            elif c_sum < target:
                left += 1
            else:
                return [left+1, right+1]