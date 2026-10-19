class Solution:
    def largestRectangleArea(self, heights: list[int]) -> int:
        stack = []
        n = len(heights)
        maxarea = 0

        for i in range(n+1):
            currheight = 0 if i == n else heights[i]

            while stack and currheight < heights[stack[-1]]:
                poppedindex = stack.pop()
                height = heights[poppedindex]

                if stack:
                    width = i - stack[-1] -1
                else:
                    width = i
                maxarea = max(maxarea, height*width)
            stack.append(i)
        return maxarea
        
