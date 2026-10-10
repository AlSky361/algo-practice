class Solution:
    def trap(self, height: list[int]) -> int:
        l, r = 0, len(height) - 1
        left_max, right_max = height[l], height[r]
        total = 0

        while l < r:
            if height[l] < height[r]:
                if height[l] >= left_max:
                    left_max = height[l]
                else:
                    total += left_max - height[l]
                l += 1
            else:
                if height[r] >= right_max:
                    right_max = height[r]
                else:
                    total += right_max - height[r]
                r -= 1


        return total
