import heapq
class Solution:
    def kSmallestPairs(self, nums1: list[int], nums2: list[int], k: int) -> list[list[int]]:
        if not nums1 or not nums2 or k==0:
            return []
        
        heap = []

        for i in range(min(k,len(nums1))):
            heapq.heappush(heap, (nums1[i]+nums2[0],i,0))
        
        result = []
        while heap and len(result) < k:
            total,i,j = heapq.heappop(heap)

            result.append([nums1[i],nums2[j]])

            if j+1 < len(nums2):
                heapq.heappush(heap, (nums1[i]+nums2[j+1], i, j+1))
            
        return result