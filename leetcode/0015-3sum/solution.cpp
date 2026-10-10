#include <vector>
#include <algorithm>

class Solution {
public:
    std::vector<std::vector<int>> threeSum(std::vector<int>& nums) {
        int n = static_cast<int>(nums.size());
        std::vector<std::vector<int>> result;
        std::sort(nums.begin(), nums.end());

        for (int i = 0; i < n - 2; i++) {
            if (nums[i] + nums[i + 1] + nums[i + 2] > 0) break;
            if (i > 0 && nums[i] == nums[i - 1]) continue;
            if (nums[i] + nums[n - 2] + nums[n - 1] < 0) continue;

            int j = i + 1, k = n - 1;

            while (j < k) {
                int total = nums[i] + nums[j] + nums[k];
                if (total < 0) {
                    j++;
                } else if (total > 0) {
                    k--;
                } else {
                    result.push_back({nums[i], nums[j], nums[k]});

                    while (j < k && nums[j] == nums[j + 1]) j++;
                    while (j < k && nums[k] == nums[k - 1]) k--;
                    j++;
                    k--;
                }
            }
        }

        return result;
    }
};
