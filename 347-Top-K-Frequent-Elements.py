class Solution:
    def topKFrequent(self, nums: list[int], k: int) -> list[int]:
        frequency = {}

        for num in nums:
            frequency[num] = frequency.get(num, 0) + 1
            
        sortedlist = sorted(frequency.items(), key = lambda items:items[1], reverse = True)

        return [items[0] for items in sortedlist[:k]]