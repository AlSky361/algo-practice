#include <algorithm>
#include <array>
#include <string>

class Solution {
public:
    int lengthOfLongestSubstring(const std::string& s) {
        std::array<int, 256> next_left{};
        int left = 0, best = 0;
        const int n = static_cast<int>(s.size());

        for (int right = 0; right < n; ++right) {
            const auto c = static_cast<unsigned char>(s[right]);

            left = std::max(left, next_left[c]);
            next_left[c] = right + 1;
            best = std::max(best, right - left + 1);
        }

        return best;
    }
};
