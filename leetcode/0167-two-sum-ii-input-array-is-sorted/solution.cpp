#include <vector>

class Solution {
public:
    std::vector<int> twoSum(std::vector<int>& numbers, int target) {
        int l = 0;
        int r = static_cast<int>(numbers.size()) - 1;

        while (l < r) {
            int total = numbers[l] + numbers[r];
            if (total > target) {
                r--;
            } else if (total < target) {
                l++;
            } else {
                return {l + 1, r + 1};
            }
        }

        return {};
    }
};
