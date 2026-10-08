class Solution:
    def containsDuplicate(self, nums: list[int]) -> bool:
        hash_set = set()

        for el in nums:
            if el in hash_set:
                return True
            hash_set.add(el)
        
        return False
