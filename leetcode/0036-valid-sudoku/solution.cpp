#include <vector>
#include <unordered_set>

class Solution {
public:
    bool isValidSudoku(std::vector<std::vector<char>>& board) {
        std::vector<std::unordered_set<char>> rows(9);
        std::vector<std::unordered_set<char>> cols(9);
        std::vector<std::unordered_set<char>> boxes(9);

        for (int row_idx = 0; row_idx < 9; row_idx++) {
            for (int col_idx = 0; col_idx < 9; col_idx++) {
                char el = board[row_idx][col_idx];

                if (el == '.') continue;

                int box_idx = (row_idx / 3) * 3 + (col_idx / 3);

                if (rows[row_idx].contains(el) || (cols[col_idx].contains(el)) || (boxes[box_idx].contains(el))) {
                    return false;
                }

                rows[row_idx].insert(el);
                cols[col_idx].insert(el);
                boxes[box_idx].insert(el);
            }
        }

        return true;
    }
};
