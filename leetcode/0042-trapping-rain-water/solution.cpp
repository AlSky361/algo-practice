#include <vector>

class Solution {
public:
    int trap(std::vector<int>& height) {
        int l = 0;
        int r = static_cast<int>(height.size()) - 1;

        int left_max = height[l];
        int right_max = height[r];

        int total = 0;

        while (l < r) {
            if (height[l] < height[r]) {
                if (height[l] > left_max) {
                    left_max = height[l];
                } else { total += left_max - height[l]; }
                l++;
            } else {
                if (height[r] > right_max) {
                    right_max = height[r];
                } else { total += right_max - height[r]; }
                r--;
            }
        }

        return total;
    }
};