class Solution:
    def eraseOverlapIntervals(self, intervals: list[list[int]]) -> int:
        if not intervals:
            return 0
        
        intervals.sort(key = lambda x:x[1])
        removals = 0
        end = intervals[0][1]

        for i in range(1,len(intervals)):
            current = intervals[i]
            
            if current[0] >= end:
                end = current[1]
            else:
                removals += 1
            
        return removals