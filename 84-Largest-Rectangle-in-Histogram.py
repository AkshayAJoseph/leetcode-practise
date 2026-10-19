class Solution:
    def largestRectangleArea(self, heights: list[int]) -> int:
        stack = []
        n = len(heights)
        maxarea = 0
        heights.append(0)

        for i,h in enumerate(heights):
            while stack and h < heights[stack[-1]]:
                height = heights[stack.pop()]

                if stack:
                    width = i - stack[-1] -1
                else:
                    width = i
                maxarea = max(maxarea, height*width)
            stack.append(i)
        return maxarea
        
