class Solution:
    def minWindow(self, s: str, t: str) -> str:
        if not s or not t:
            return ""
        
        required = {}
        min_len = float('inf')
        min_start = 0

        for ch in t:
            required[ch] = required.get(ch, 0) + 1
        
        window = {}
        left = 0
        formed = 0

        for right,ch in enumerate(s):
            window[ch] = window.get(ch, 0) + 1
            
            if ch in required and required[ch] == window[ch]:
                formed += 1
            
            while formed == len(required):
                if right - left + 1 < min_len:
                    min_len = right - left + 1
                    min_start = left

                window[s[left]] -= 1

                if s[left] in required and window[s[left]] < required[s[left]]:
                    formed -= 1
                
                left += 1
        if min_len == float('inf'):
            return ""

        return (s[min_start:min_start + min_len])
