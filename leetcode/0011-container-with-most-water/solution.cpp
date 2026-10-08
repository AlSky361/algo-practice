#include <vector>
#include <algorithm>

class Solution {
public:
    int maxArea(std::vector<int>& height) {
        int l = 0, best = 0;
        int r = static_cast<int>(height.size()) - 1;
        int max_h = *max_element(height.begin(), height.end());

        while (l < r && best < max_h * (r - l)) {
            int local = std::min(height[r], height[l]) * (r - l);
            best = std::max(best, local);

            if (height[l] < height[r]) {
                l++;
            } else {
                r--;
            }
        }

        return best;
    }
};
