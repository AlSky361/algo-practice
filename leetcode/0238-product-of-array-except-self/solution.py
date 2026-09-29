class Solution:
    def productExceptSelf(self, nums: list[int]) -> list[int]:
        n = len(nums)
        zero_idx = None
        prod = 1

        for i, el in enumerate(nums):
            if el != 0:
                prod *= el
            else:
                if zero_idx is not None:
                    return [0] * n
                zero_idx = i
        
        if zero_idx is not None:
            result = [0] * n
            result[zero_idx] = prod
            return result

        result = [1] * n
        left = right = 1

        for i in range(n):
            j = n - 1 - i

            result[i] *= left
            left *= nums[i]

            result[j] *= right
            right *= nums[j]

        return result