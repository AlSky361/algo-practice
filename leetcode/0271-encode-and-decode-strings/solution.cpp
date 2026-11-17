#include <cstddef>
#include <string>
#include <vector>

class Solution {
public:
    std::string encode(const std::vector<std::string>& strs) {
        std::string encoded;
        for (const auto& part : strs) {
            encoded += std::to_string(part.size()) + '/' + part;
        }
        return encoded;
    } 

    std::vector<std::string> decode(const std::string& encoded) {
        std::vector<std::string> decoded;
        std::size_t i = 0;

        while (i < encoded.size()) {
            const auto slash = encoded.find('/', i);
            const auto n = std::stoul(encoded.substr(i, slash - i));
            const auto start = slash + 1;

            decoded.emplace_back(encoded, start, n);
            i = start + n;
        }

        return decoded;
    }
};
