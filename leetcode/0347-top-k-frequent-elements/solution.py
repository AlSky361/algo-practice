from collections import Counter

class Solution:
    def topKFrequent(self, nums: list[int], k: int) -> list[int]:
        freq_arr = Counter(nums).most_common(k)
        result = []

        for key, _ in freq_arr:
            result.append(key)
        
        return result
