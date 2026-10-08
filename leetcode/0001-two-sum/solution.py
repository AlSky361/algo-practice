class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:
        hash_map = {}

        for i, el in enumerate(nums):
            if (predict := target - el) in hash_map:
                return [hash_map[predict], i]
            hash_map[el] = i
        
        return []
