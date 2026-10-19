class Solution:
    def nextGreaterElement(self, nums1: list[int], nums2: list[int]) -> list[int]:
        stack = []
        greater = {}

        for num in nums2:
            while stack and num > stack[-1]:
                small = stack.pop()
                greater[small] = num
            
            stack.append(num)
        
        result = []
        for num in nums1:
            result.append(greater.get(num, -1))

        return result