class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        last_seen = {}
        best, left = 0, 0

        for right, c in enumerate(s):
            previous = last_seen.get(c, -1)
            left = max(left, previous + 1)
            last_seen[c] = right
            best = max(best, right - left + 1)
        
        return best
