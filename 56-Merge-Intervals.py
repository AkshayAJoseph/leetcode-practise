class Solution:
    def merge(self, intervals: list[list[int]]) -> list[list[int]]:
        intervals.sort()
        merged = []

        for current in intervals:
            if merged and current[0] <= merged[-1][1]:
                merged[-1][1] = max(merged[-1][1], current[1])
            else:
                merged.append(current)
        
        return merged