#include <vector>
#include <unordered_set>
#include <algorithm>

class Solution {
public:
    int longestConsecutive(std::vector<int>& nums) {
        const std::unordered_set<int> num_set(nums.begin(), nums.end());
        const int total = static_cast<int>(nums.size());
        int best = 0;

        for (int el : nums) {
            if (num_set.contains(el - 1)) {
                continue;
            }

            int current = el;
            while (num_set.contains(current + 1)) {
                current++;
            }

            best = std::max(best, current - el + 1);

            if (2 * best >= total) {
                break;
            }
        }

        return best;
    }
};
