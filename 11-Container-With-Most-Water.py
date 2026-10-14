class Solution:
    def maxArea(self, height: list[int]) -> int:
        l_area = 0
        n = len(height)
        left = 0
        right = n-1
        
        while left < right:
            area = min(height[left],height[right]) * (right - left)
            l_area = max(l_area, area)
            if height[left] < height[right]:
                left += 1
            else:
                right -= 1
        return l_area
                