from copy import deepcopy
import random


class Sudoku:
    def __init__(self, initial_board):
        self.sudoku_numbers = deepcopy(initial_board)
        self.possible_values = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        self.changeable_numbers = [[initial_board[y][x] not in self.possible_values for x in range(9)] for y in
                                   range(9)]
        self.solved_sudoku_numbers = deepcopy(initial_board)

    def get_square(self, pos_x, pos_y):
        sq_x = 3 * (pos_x // 3)
        sq_y = 3 * (pos_y // 3)
        return sq_x, sq_y

    def next_pos(self, pos_x, pos_y):
        return next(((x, y) for x in range(pos_x, 9) for y in range(pos_y, 9) if
                     self.solved_sudoku_numbers[x][y] not in self.possible_values), None) \
               or next(((x, y) for x in range(9) for y in range(9) if
                        self.solved_sudoku_numbers[x][y] not in self.possible_values), (-1, -1))

    def check_move(self, i, j, value):
        check_row = all([self.solved_sudoku_numbers[i][x] != value for x in range(9)])
        check_col = all([self.solved_sudoku_numbers[x][j] != value for x in range(9)])
        sq_x, sq_y = self.get_square(i, j)
        check_square = all(
            [self.solved_sudoku_numbers[x][y] != value for x in range(sq_x, sq_x + 3) for y in range(sq_y, sq_y + 3)])
        return check_row and check_col and check_square

    def solve_sudoku(self, pos_x=0, pos_y=0):
        pos_x, pos_y = self.next_pos(pos_x, pos_y)
        if pos_x == -1 and pos_y == -1:
            return True
        for value in self.possible_values:
            if self.check_move(pos_x, pos_y, value):
                self.solved_sudoku_numbers[pos_x][pos_y] = value
                if self.solve_sudoku(pos_x, pos_y):
                    return True
                self.solved_sudoku_numbers[pos_x][pos_y] = None
        return False

    def check_sudoku(self):
        for i in range(9):
            row = self.sudoku_numbers[i]
            column = [row[i] for row in self.sudoku_numbers]
            row_values = list(filter(lambda x: x in self.possible_values, row))
            col_values = list(filter(lambda x: x in self.possible_values, column))
            check_row = len(row_values) == len(set(row_values))
            check_col = len(col_values) == len(set(col_values))
            if not check_row or not check_col:
                return False
        for sq_x in range(0, 9, 3):
            for sq_y in range(0, 9, 3):
                square = [self.sudoku_numbers[i][j] for i in range(sq_x, sq_x + 3) for j in range(sq_y, sq_y + 3)]
                square_values = list(filter(lambda x: x in self.possible_values, square))
                if len(square_values) != len(set(square_values)):
                    return False
        numbers = [[self.sudoku_numbers[x][y] in self.possible_values for x in range(9)] for y in range(9)]
        valid_numbers = 0
        for i in range(9):
            valid_numbers += sum(numbers[i])
        if valid_numbers == 81:
            return "all"
        return "ok"

    def change_value(self, i, j, value):
        self.sudoku_numbers[i][j] = value

    def get_hint(self):
        self.solved_sudoku_numbers = deepcopy(self.sudoku_numbers)
        if self.solve_sudoku():
            free_positions = [(i, j) for i in range(9) for j in range(9) if
                              self.sudoku_numbers[i][j] not in self.possible_values]
            i, j = random.choice(free_positions)
            self.change_value(i, j, self.solved_sudoku_numbers[i][j])
            return i, j, self.solved_sudoku_numbers[i][j]
        return None

    def reset_sudoku(self):
        self.sudoku_numbers = deepcopy(
            [[self.sudoku_numbers[y][x] if not self.changeable_numbers[y][x] else None for x in range(9)] for y in
             range(9)])
