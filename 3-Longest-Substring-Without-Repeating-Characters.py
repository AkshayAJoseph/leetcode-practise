class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        start = 0
        seen = {}
        max_len = 0

        for end, ch in enumerate(s):
            if ch in seen and seen[ch] >= start:
                start = seen[ch] + 1

            seen[ch] = end
            max_len = max(max_len, end - start + 1)

        return max_len