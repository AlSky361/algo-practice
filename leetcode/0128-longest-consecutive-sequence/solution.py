class Solution:
    def longestConsecutive(self, nums: list[int]) -> int:
        num_set = set(nums)
        total = len(num_set)
        best = 0

        for el in num_set:
            if el - 1 in num_set:
                continue

            current = el
            while current + 1 in num_set:
                current += 1

            best = max(best, current - el + 1)

            if 2 * best >= total:
                break

        return best
