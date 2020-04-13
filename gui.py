from tkinter import *
from tkinter.font import Font
from tkinter import messagebox
import copy
import random


# configuration ###################################

class Sudoku:
    def __init__(self, initial_board):
        self.sudoku_numbers = copy.deepcopy(initial_board)
        self.possible_values = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        self.changeable_numbers = [[initial_board[x][y] not in self.possible_values for x in range(9)] for y in range(9)]
        self.solved_sudoku_numbers = copy.deepcopy(initial_board)

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
                self.solved_sudoku_numbers[pos_x][pos_y] = 0
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
        numbers = [[self.sudoku_numbers[x][y] not in self.possible_values for x in range(9)] for y in range(9)]
        return len(numbers) == 64

    def change_value(self, i, j, value):
        self.sudoku_numbers[i][j] = value

    def get_hint(self):
        self.solved_sudoku_numbers = copy.deepcopy(self.sudoku_numbers)
        if self.solve_sudoku():
            free_positions = [(i, j) for i in range(9) for j in range(9) if
                              self.sudoku_numbers[i][j] not in self.possible_values]
            i, j = random.choice(free_positions)
            self.change_value(i, j, self.solved_sudoku_numbers[i][j])
            return i, j, self.solved_sudoku_numbers[i][j]
        return None



class SudokuBoard:
    def __init__(self, state, initial_sudoku):
        self.sudoku_board = Canvas(state.app, width=state.set_width(1 / 2), height=state.set_height(0.75), bd=0,
                                   highlightbackground="black", highlightthickness=5)
        self.horizontal_lines = []
        self.vertical_lines = []
        self.sudoku = Sudoku(initial_sudoku)
        self.numbers = []
        self.zero_font_color = "#636e72"
        self.number_font_color = "#2d3436"

    def set_initial_sudoku_board(self, scale36, scale18, scale2, bigger_font):
        for row, line in enumerate(self.sudoku.sudoku_numbers):
            numbers_in_row = []
            for column, number in enumerate(line):
                string_number = str(number) if number in self.sudoku.possible_values else " "
                string_color = self.number_font_color if number in self.sudoku.possible_values else self.zero_font_color
                background = self.sudoku_board.create_rectangle(column * scale18, row * scale18,
                                                                column * scale18 + scale18, row * scale18 + scale18,
                                                                fill="white", outline="white")

                text = self.sudoku_board.create_text(column * scale18 + scale36, row * scale18 + scale36,
                                                     text=string_number, fill=string_color,
                                                     font=bigger_font)

                numbers_in_row.append([background, text])
            self.numbers.append(numbers_in_row)

        for index in range(1, 9):
            self.vertical_lines.append(
                self.sudoku_board.create_line(index * scale18, 0, index * scale18, scale2, fill="black",
                                              width=(5 if index % 3 == 0 else 2)))
            self.horizontal_lines.append(
                self.sudoku_board.create_line(0, index * scale18, scale2, index * scale18, fill="black",
                                              width=(5 if index % 3 == 0 else 2)))

    def get_hint(self):
        hint = self.sudoku.get_hint()
        if hint:
            i, j, value = hint
            self.sudoku_board.itemconfig(
                self.numbers[i][j][1], text=str(value))

    def check(self):
        is_completed = self.sudoku.check_sudoku()
        if is_completed:
            messagebox.showinfo("Congratulation!", "You've completed sudoku!")
        else:
            messagebox.showinfo(":(", "Try again! You have some mistakes.")


class State:

    def __init__(self, initial_sudoku_numbers):
        self.app = Tk()
        self.selected_row = None
        self.selected_column = None
        self.window_size_width = 1500
        self.window_size_height = 1000
        self.font_size = int(self.window_size_height / 25)
        self.field_color = "#f0f1f5"
        self.normal_font = Font(family="Open Sans", size=self.font_size)
        self.bigger_font = Font(family="Open Sans", size=self.set_font(3 / 2))
        self.sudoku_table = SudokuBoard(self, initial_sudoku_numbers)
        self.number_buttons = []
        self.help_buttons = []
        self.main_buttons = []
        self.number_buttons_frame = Frame(self.app, width=self.set_width(1 / 10), height=self.set_height(1 / 2))
        self.help_buttons_frame = Frame(self.app, width=self.set_width(1 / 10), height=self.set_height(1 / 2))
        self.main_buttons_frame = Frame(self.app, width=self.set_width(1 / 5), height=self.window_size_height)
        self.info_frame = Frame(self.app, width=self.set_width(1 / 5), height=self.window_size_height)

    def set_width(self, scale):
        return int(self.window_size_width * scale)

    def set_height(self, scale):
        return int(self.window_size_height * scale)

    def set_font(self, scale):
        return int(self.font_size * scale)

    def actualize_font(self):
        self.normal_font = Font(family="Open Sans", size=self.font_size)
        self.bigger_font = Font(family="Open Sans", size=self.set_font(3 / 2))

    def set_number_buttons(self):
        for index in range(10):
            self.number_buttons.append(Button(self.number_buttons_frame, text="NONE" if index == 0 else index,
                                              font=self.normal_font))
            self.number_buttons[index].bind("<Button-1>", lambda event, num=index: self.set_sudoku_number(event, num))
            self.number_buttons[index].pack(side=LEFT)

    def set_help_buttons(self):
        self.help_buttons.append(
            Button(self.help_buttons_frame, text="CHECK", command=lambda: self.sudoku_table.check(), font=self.normal_font))
        self.help_buttons.append(
            Button(self.help_buttons_frame, text="HINT", command=lambda: self.sudoku_table.get_hint(),
                   font=self.normal_font))
        self.help_buttons.append(Button(self.help_buttons_frame, text="SOMETHING",font=self.normal_font))

    def set_main_buttons(self):
        self.main_buttons.append(
            Button(self.main_buttons_frame, text="QUIT", command=self.app.destroy, font=self.normal_font))
        for button_text in ["IMPORT", "RESET", "HIGH SCORES"]:
            self.main_buttons.append(Button(self.main_buttons_frame, text=button_text, font=self.normal_font))

    def set_sudoku_number(self, event, number):
        print(self.selected_row, self.sudoku_table.sudoku.changeable_numbers[self.selected_row][self.selected_column])
        if self.selected_row is not None and self.sudoku_table.sudoku.changeable_numbers[self.selected_row][self.selected_column]:
            string_number = "  " if number == 0 else str(number)
            print(string_number)

            self.sudoku_table.sudoku_board.itemconfig(self.sudoku_table.numbers[self.selected_row][self.selected_column][1], text=string_number)
            self.sudoku_table.sudoku.change_value(self.selected_row, self.selected_column, number)

    def select_field(self, event):
        column = int(event.x / self.set_width(1 / 18))
        row = int(event.y / self.set_width(1 / 18))

        if not self.sudoku_table.sudoku.changeable_numbers[row][column]: return

        if self.selected_row is not None:
            self.sudoku_table.sudoku_board.itemconfig(self.sudoku_table.numbers[self.selected_row][self.selected_column][0], fill="white")

        self.selected_row = row
        self.selected_column = column

        self.sudoku_table.sudoku_board.itemconfig(self.sudoku_table.numbers[row][column][0], fill=self.field_color)

    def place(self):
        scale2w = self.set_width(1 / 2)
        scale4w = self.set_width(1 / 4)
        scale5w = self.set_width(1 / 5)
        scale10w = self.set_width(1 / 10)
        scale18w = self.set_width(1 / 18)
        scale36w = self.set_width(1 / 36)
        scale2h = self.set_height(1 / 2)

        self.font_size = self.set_height(1 / 25)

        self.number_buttons_frame.config(width=scale10w, height=scale2h)
        self.help_buttons_frame.config(width=scale10w, height=scale2h)
        self.main_buttons_frame.config(width=scale5w, height=self.window_size_height)
        self.info_frame.config(width=scale5w, height=self.window_size_height)
        self.sudoku_table.sudoku_board.config(width=scale2w, height=self.set_height(0.75))

        self.sudoku_table.sudoku_board.place(x=scale4w, y=0)
        self.number_buttons_frame.place(x=scale4w, y=self.set_height(0.8))
        self.help_buttons_frame.place(x=scale4w, y=self.set_height(0.9))
        self.info_frame.place(x=self.set_width(0.8), y=0)
        self.main_buttons_frame.place(x=0, y=0)

        for index, button in enumerate(self.main_buttons):
            button.place(x=0, y=index * self.set_height(0.065), width=scale5w)
            button.config(font=self.normal_font)

        for index, button in enumerate(self.help_buttons):
            button.place(x=index * self.set_height(1 / 6), y=0, width=scale5w)
            button.config(font=self.normal_font)

        for button in self.number_buttons:
            button.config(font=self.normal_font)

        for index, line in enumerate(self.sudoku_table.vertical_lines):
            self.sudoku_table.sudoku_board.coords(line, (index + 1) * scale18w, 0, (index + 1) * scale18w, scale2w)

        for index, line in enumerate(self.sudoku_table.horizontal_lines):
            self.sudoku_table.sudoku_board.coords(line, 0, (index + 1) * scale18w, scale2w, (index + 1) * scale18w)

        for row, line in enumerate(self.sudoku_table.numbers):
            for column, field in enumerate(line):
                self.sudoku_table.sudoku_board.coords(field[0], column * scale18w, row * scale18w,
                                         column * scale18w + scale18w, row * scale18w + scale18w)
                self.sudoku_table.sudoku_board.coords(field[1], column * scale18w + scale36w, row * scale18w + scale36w)
                self.sudoku_table.sudoku_board.itemconfig(self.sudoku_table.numbers[row][column][1],
                                             font=self.bigger_font)

    def set_initial_sudoku_board(self):
        scale36 = self.set_width(1 / 36)
        scale18 = self.set_width(1 / 18)
        scale2 = self.set_width(1 / 2)
        self.sudoku_table.set_initial_sudoku_board(scale36, scale18, scale2, self.bigger_font)

initial_sudoku_numbers = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
                            [6, 0, 0, 1, 9, 5, 0, 0, 0],
                            [0, 9, 8, 0, 0, 0, 0, 6, 0],
                            [8, 0, 0, 0, 6, 0, 0, 0, 3],
                            [4, 0, 0, 8, 0, 3, 0, 0, 1],
                            [7, 0, 0, 0, 2, 0, 0, 0, 6],
                            [0, 6, 0, 0, 0, 0, 2, 8, 0],
                            [0, 0, 0, 4, 1, 9, 0, 0, 5],
                            [0, 0, 0, 0, 8, 0, 0, 7, 9]]
state = State(initial_sudoku_numbers)


# main #############################################


def main():
    state.app.title('Sudoku solver!')
    state.app.geometry(str(state.window_size_width) + "x" + str(state.window_size_height))

    state.sudoku_table.sudoku_board.bind("<Button-1>", state.select_field)
    state.set_initial_sudoku_board()

    state.set_number_buttons()
    state.set_help_buttons()
    state.set_main_buttons()

    state.place()

    while True:
        state.app.update()
        if state.window_size_width != state.app.winfo_width() or state.window_size_height != state.window_size_height:
            if state.app.winfo_width() * 2 / 3 > state.app.winfo_height():
                state.window_size_width = int(state.app.winfo_height() * 3 / 2)
                state.window_size_height = state.app.winfo_height()
                state.actualize_font()
            else:
                state.window_size_width = state.app.winfo_width()
                state.window_size_height = int(state.app.winfo_width() * 2 / 3)

            state.app.geometry(str(state.window_size_width) + "x" + str(state.window_size_height))
            state.place()


if __name__ == "__main__":
    main()

# solved ############################################

# [[5, 3, 4, 6, 7, 8, 9, 1, 2],
#  [6, 7, 2, 1, 9, 5, 3, 4, 8],
#  [1, 9, 8, 3, 4, 2, 5, 6, 7],
#  [8, 5, 9, 7, 6, 1, 4, 2, 3],
#  [4, 2, 6, 8, 5, 3, 7, 9, 1],
#  [7, 1, 3, 9, 2, 4, 8, 5, 6],
#  [9, 6, 1, 5, 3, 7, 2, 8, 4],
#  [2, 8, 7, 4, 1, 9, 6, 3, 5],
#  [3, 4, 5, 2, 8, 6, 1, 7, 9]] changable_numebrs = [[False for x in range(9)] for y in range(9)]
