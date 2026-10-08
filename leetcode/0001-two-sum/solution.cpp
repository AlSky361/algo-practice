#include <vector>
#include <unordered_map>

class Solution {
public:
    std::vector<int> twoSum(std::vector<int>& nums, int target) {
        std::unordered_map<int, int> hash_map;

        for (int i = 0; i < nums.size(); i++) {
            int el = nums[i];
            int predict = target - el;
            if (hash_map.contains(predict)) {
                return {hash_map[predict], i};
            }
            hash_map[el] = i;
        }

        return {};
    }
};
