from collections import defaultdict

class Solution:
    def groupAnagrams(self, strs: list[str]) -> list[list[str]]:
        hash_map = defaultdict(list)

        for s in strs:
            hash_s = "".join(sorted(s))
            hash_map[hash_s].append(s)
        
        return list(hash_map.values())
