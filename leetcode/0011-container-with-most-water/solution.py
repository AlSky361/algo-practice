class Solution:
    def maxArea(self, height: list[int]) -> int:
        l, r = 0, len(height) - 1
        best = 0
        max_h = max(height)

        while l < r and best < max_h * (r - l):
            local = min(height[l], height[r]) * (r - l)
            best = max(best, local)

            if height[l] < height[r]:
                l += 1
            else:
                r -= 1
        
        return best