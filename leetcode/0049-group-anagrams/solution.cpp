#include <vector>
#include <string>
#include <unordered_map>

class Solution {
public:
    std::vector<std::vector<std::string>> groupAnagrams(std::vector<std::string> strs) {
        std::unordered_map<std::string, std::vector<std::string>> hash_map;

        for (std::string& s : strs) {
            std::string sorted_s = s;
            sort(sorted_s.begin(), sorted_s.end());
            hash_map[sorted_s].push_back(move(s));
        }

        std::vector<std::vector<std::string>> result;
        result.reserve(hash_map.size());

        for (auto& pair : hash_map) {
            result.push_back(move(pair.second));
        }

        return result;
    }
};
