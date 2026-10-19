class Solution:
    def findMin(self, nums: list[int]) -> int:
        left = 0
        right = len(nums) - 1

        while left < right:
            mid = (right + left) // 2

            if nums[mid] <= nums[right]:
                right = mid
            else:
                left = mid + 1
            
        return nums[right]