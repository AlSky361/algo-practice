#include <string>
#include <vector>

class Solution {
public:
    bool isAnagram(std::string s, std::string t) {
        if (s.size() != t.size()) {
            return false;
        }

        std::vector<int> counts(26);

        for (char c : s) {
            counts[c - 'a'] ++;
        }

        for (char c : t) {
            if (counts[c - 'a'] == 0) {
                return false;
            }
            counts[c - 'a'] --;
        }

        return true;
    }
};
