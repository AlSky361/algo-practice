class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False

        set_s, set_t = set(s), set(t)

        if len(set_s) != len(set_t):
            return False

        for el in set_s:
            if s.count(el) != t.count(el):
                return False
        
        return True
