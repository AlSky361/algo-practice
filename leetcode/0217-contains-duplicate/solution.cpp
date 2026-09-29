#include <vector>
#include <unordered_set>

class Solution {
public:
    bool containsDuplicate(std::vector<int>& nums) {
        std::unordered_set<int> hash_set;
        hash_set.reserve(nums.size());

        for (int el : nums) {
            if (!hash_set.insert(el).second) {
                return true;
            }
        }

        return false;
    }
};