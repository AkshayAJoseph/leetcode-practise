class Solution:
    def findMaxLength(self, nums: List[int]) -> int:
        balance = 0
        first_seen = {
            0:-1
        }
        max_len = 0
        for i in range (len(nums)):
            if nums[i] == 0:
                balance -= 1
            else:
                balance +=1
            if balance in first_seen:
                curr_len = i - first_seen[balance]
                max_len = max(curr_len, max_len)
            else:
                first_seen[balance] = i
        return max_len