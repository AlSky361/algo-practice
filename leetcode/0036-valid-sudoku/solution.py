class Solution:
    def isValidSudoku(self, board: list[list[str]]) -> bool:
        rows = [set() for _ in range(9)]
        cols = [set() for _ in range(9)]
        boxes = [set() for _ in range(9)]

        for row_idx in range(9):
            for col_idx in range(9):
                el = board[row_idx][col_idx]

                if el == ".":
                    continue

                box_idx = (row_idx // 3) * 3 + col_idx // 3

                if (el in rows[row_idx]) or (el in cols[col_idx]) or (el in boxes[box_idx]):
                    return False

                rows[row_idx].add(el)
                cols[col_idx].add(el)
                boxes[box_idx].add(el)
                
        return True
