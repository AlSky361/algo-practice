#include <vector>

class Solution {
public:
    int maxProfit(std::vector<int>& prices) {
        int min_price = prices[0];
        int best = 0;

        for (int price : prices) {
            if (price < min_price) {
                min_price = price;
            } else if (price - min_price > best) {
                best = price - min_price;
            }
        }

        return best;
    }
};
