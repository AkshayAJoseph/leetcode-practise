class Solution:
    def findMaxAverage(self, nums: list[int], k: int) -> float:
        window_s = sum(nums[:k])
        max_s = window_s
        for i in range(0, len(nums)-k):
            window_s = window_s - nums[i] + nums[i+k]
            max_s = max(max_s , window_s)
        
        return max_s/k