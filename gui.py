from tkinter import *
from tkinter.font import Font
from sudoku_board import SudokuBoard

# TODO: fix highscores
# TODO: import - choose source and get it from your memory
# TODO: refactor sudoku and refactor state

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
            Button(self.help_buttons_frame, text="HINT", command=lambda: self.sudoku_table.get_hint(),
                   font=self.normal_font))
        self.help_buttons.append(
            Button(self.help_buttons_frame, text="CHECK", command=lambda: self.sudoku_table.check(), font=self.normal_font))
        self.help_buttons.append(Button(self.help_buttons_frame, text="FIELD",font=self.normal_font))

    def set_main_buttons(self):
        self.main_buttons.append(
            Button(self.main_buttons_frame, text="QUIT", command=self.app.destroy, font=self.normal_font))
        self.main_buttons.append(
            Button(self.main_buttons_frame, text="RESET", command=lambda: self.reset_sudoku_board(), font=self.normal_font))
        self.main_buttons.append(Button(self.main_buttons_frame, text="HIGH SCORES", command=lambda: self.sudoku_table.get_scores(), font=self.normal_font))
        self.main_buttons.append(Button(self.main_buttons_frame, text="IMPORT", font=self.normal_font))

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
        self.help_buttons_frame.config(width=scale5w*3, height=scale2h)
        self.main_buttons_frame.config(width=scale5w, height=self.window_size_height)
        self.info_frame.config(width=scale5w, height=self.window_size_height)
        self.sudoku_table.sudoku_board.config(width=scale2w, height=self.set_height(0.75))

        self.sudoku_table.sudoku_board.place(x=scale4w, y=0)
        self.number_buttons_frame.place(x=scale4w, y=self.set_height(0.8))
        self.help_buttons_frame.place(x=scale4w, y=self.set_height(0.9))
        self.info_frame.place(x=self.set_width(0.8), y=0)
        self.main_buttons_frame.place(x=0, y=0)

        for index, button in enumerate(self.main_buttons):
            #button.place(x=0, y=index * self.set_height(0.065), width=scale5w)
            button.place(x=0, y=index * self.set_height(0.085), width=scale5w)
            button.config(font=self.normal_font)

        for index, button in enumerate(self.help_buttons):
            button.place(x=index * self.set_width(1 / 6), y=0, width=scale5w)
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

    def reset_sudoku_board(self):
        scale36 = self.set_width(1 / 36)
        scale18 = self.set_width(1 / 18)
        scale2 = self.set_width(1 / 2)
        self.sudoku_table.reset_board(scale36, scale18, scale2, self.bigger_font)


def main():
    initial_sudoku_numbers = [[None, 8, None, None, 1, 3, 4, None, None],
                              [4, 2, 3, 6, 8, None, None, None, None],
                              [None, 7, 1, None, 5, 4, None, 8, 3],
                              [1, 9, None, None, None, 8, 7, None, None],
                              [None, 4, 7, None, None, 2, 5, None, 8],
                              [None, 5, None, None, None, 9, None, 3, None],
                              [2, None, 9, 3, None, 5, None, 7, None],
                              [5, None, None, 7, 2, None, None, None, 9],
                              [7, 3, None, None, None, None, 2, None, 6]]
    state = State(initial_sudoku_numbers)
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

            else:
                state.window_size_width = state.app.winfo_width()
                state.window_size_height = int(state.app.winfo_width() * 2 / 3)
            state.actualize_font()
            state.app.geometry(str(state.window_size_width) + "x" + str(state.window_size_height))
            state.place()

if __name__ == "__main__":
    main()

