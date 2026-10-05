class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        count = 0
        prefix_count = {
            0:1
        }
        prefix = 0

        for i in range (len(nums)):
            prefix += nums[i]
            required = prefix - k
            count += prefix_count.get(required, 0)
            prefix_count[prefix] = prefix_count.get(prefix, 0) + 1
        return count