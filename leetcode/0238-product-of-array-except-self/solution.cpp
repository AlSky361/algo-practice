#include <vector>

class Solution {
public:
    std::vector<int> productExceptSelf(std::vector<int>& nums) {
        const int n = static_cast<int>(nums.size());
        int zero_idx = -1;
        int prod = 1;

        for (int i = 0; i < n; i++) {
            const int el = nums[i];
            if (el != 0) {
                prod *= el;
            } else {
                if (zero_idx != -1) {
                    return std::vector<int>(n, 0);
                }
                zero_idx = i;
            }
        }

        if (zero_idx != -1) {
            std::vector<int> result(n, 0);
            result[zero_idx] = prod;
            return result;
        }

        std::vector<int> result(n, 1);
        int left = 1, right = 1;

        for (int i = 0; i < n; i++) {
            int j = n - 1 - i;
            result[i] *= left;
            left *= nums[i];
            result[j] *= right;
            right *= nums[j];
        }

        return result;
    }
};
