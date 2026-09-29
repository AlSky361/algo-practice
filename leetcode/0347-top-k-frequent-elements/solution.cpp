#include <vector>
#include <unordered_map>
#include <cstddef>

class Solution {
public:
    std::vector<int> topKFrequent(std::vector<int>& nums, int k) {
        const int n = static_cast<int>(nums.size());
        const std::size_t limit = k;

        std::unordered_map<int, int> freq;
        for (int el : nums) {
            freq[el]++;
        }

        std::vector<std::vector<int>> buckets(n + 1);
        for (auto& [el, cnt] : freq) {
            buckets[cnt].push_back(el);
        }

        std::vector<int> result;
        result.reserve(limit);

        for (int c = n; c > 0 && result.size() < limit; c--) {
            for (int el : buckets[c]) {
                result.push_back(el);
                if (result.size() == limit) break;
            }
        }

        return result;
    }
};
