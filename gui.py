from tkinter import *
from tkinter.font import Font


# configuration ####################################


class State:

    def __init__(self):
        self.app = Tk()

        self.selected_row = None
        self.selected_column = None

        self.window_size_width = 1500
        self.window_size_height = 1000
        self.font_size = int(self.window_size_height / 25)

        self.initial_sudoku_numbers = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
                                       [6, 0, 0, 1, 9, 5, 0, 0, 0],
                                       [0, 9, 8, 0, 0, 0, 0, 6, 0],
                                       [8, 0, 0, 0, 6, 0, 0, 0, 3],
                                       [4, 0, 0, 8, 0, 3, 0, 0, 1],
                                       [7, 0, 0, 0, 2, 0, 0, 0, 6],
                                       [0, 6, 0, 0, 0, 0, 2, 8, 0],
                                       [0, 0, 0, 4, 1, 9, 0, 0, 5],
                                       [0, 0, 0, 0, 8, 0, 0, 7, 9]]
        self.sudoku_numbers = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
                               [6, 0, 0, 1, 9, 5, 0, 0, 0],
                               [0, 9, 8, 0, 0, 0, 0, 6, 0],
                               [8, 0, 0, 0, 6, 0, 0, 0, 3],
                               [4, 0, 0, 8, 0, 3, 0, 0, 1],
                               [7, 0, 0, 0, 2, 0, 0, 0, 6],
                               [0, 6, 0, 0, 0, 0, 2, 8, 0],
                               [0, 0, 0, 4, 1, 9, 0, 0, 5],
                               [0, 0, 0, 0, 8, 0, 0, 7, 9]]

        self.changeable_numbers = []
        self.numbers = []
        self.number_buttons = []
        self.help_buttons = []
        self.main_buttons = []
        self.horizontal_lines = []
        self.vertical_lines = []

        self.number_buttons_frame = Frame(self.app, width=self.set_width(1 / 10), height=self.set_height(1 / 2))
        self.help_buttons_frame = Frame(self.app, width=self.set_width(1 / 10), height=self.set_height(1 / 2))
        self.main_buttons_frame = Frame(self.app, width=self.set_width(1 / 5), height=self.window_size_height)
        self.info_frame = Frame(self.app, width=self.set_width(1 / 5), height=self.window_size_height)
        self.sudoku_board = Canvas(self.app, width=self.set_width(1 / 2), height=self.set_height(0.75),
                                   bd=0, highlightbackground="black", highlightthickness=5)

    def set_width(self, scale):
        return int(self.window_size_width * scale)

    def set_height(self, scale):
        return int(self.window_size_height * scale)

    def set_font(self, scale):
        return int(self.font_size * scale)

    def set_changeable_numbers(self):
        for row in self.sudoku_numbers:
            row_changeable_numbers = []

            for number in row:
                row_changeable_numbers.append(number == 0)

            self.changeable_numbers.append(row_changeable_numbers)

    def set_initial_sudoku_board(self):
        scale36 = self.set_width(1 / 36)
        scale18 = self.set_width(1 / 18)
        scale2 = self.set_width(1 / 2)

        for row, line in enumerate(self.initial_sudoku_numbers):
            numbers_in_row = []
            for column, number in enumerate(line):
                string_number = "  " if number == 0 else str(number)
                string_color = "#636e72" if number == 0 else "#2d3436"

                background = self.sudoku_board.create_rectangle(column * scale18, row * scale18,
                                                                column * scale18 + scale18, row * scale18 + scale18,
                                                                fill="white", outline="white")

                text = self.sudoku_board.create_text(column * scale18 + scale36,
                                                     row * scale18 + scale36,
                                                     text=string_number, fill=string_color,
                                                     font=Font(family="Open Sans", size=self.set_font(3 / 2)))

                numbers_in_row.append([background, text])

            self.numbers.append(numbers_in_row)

        for index in range(1, 9):
            self.vertical_lines.append(self.sudoku_board.create_line(index * scale18, 0,
                                                                     index * scale18, scale2,
                                                                     fill="black",
                                                                     width=(5 if index % 3 == 0 else 2)))

        for index in range(1, 9):
            self.horizontal_lines.append(self.sudoku_board.create_line(0, index * scale18,
                                                                       scale2, index * scale18,
                                                                       fill="black",
                                                                       width=(5 if index % 3 == 0 else 2)))

    def set_number_buttons(self):
        for index in range(10):
            self.number_buttons.append(Button(self.number_buttons_frame, text="NONE" if index == 0 else index,
                                              font=Font(family="Open Sans", size=self.font_size)))
            self.number_buttons[index].bind("<Button-1>", lambda event, num=index: self.set_sudoku_number(event, num))
            self.number_buttons[index].pack(side=LEFT)

    def set_help_buttons(self):
        self.help_buttons.append(Button(self.help_buttons_frame, text="HINT",
                                        font=Font(family="Open Sans", size=self.font_size)))

        self.help_buttons.append(Button(self.help_buttons_frame, text="CHECK",
                                        font=Font(family="Open Sans", size=self.font_size)))

        self.help_buttons.append(Button(self.help_buttons_frame, text="SOMETHING",
                                        font=Font(family="Open Sans", size=self.font_size)))

    def set_main_buttons(self):
        self.main_buttons.append(Button(self.main_buttons_frame, text="QUIT", command=self.app.destroy,
                                        font=Font(family="Open Sans", size=self.font_size)))

        self.main_buttons.append(Button(self.main_buttons_frame, text="IMPORT",
                                        font=Font(family="Open Sans", size=self.font_size)))

        self.main_buttons.append(Button(self.main_buttons_frame, text="RESET",
                                        font=Font(family="Open Sans", size=self.font_size)))

        self.main_buttons.append(Button(self.main_buttons_frame, text="HIGH SCORES",
                                        font=Font(family="Open Sans", size=self.font_size)))

    def set_sudoku_number(self, event, number):
        print(self.selected_row,self.changeable_numbers[self.selected_row][self.selected_column])
        if self.selected_row is not None and self.changeable_numbers[self.selected_row][self.selected_column]:
            string_number = "  " if number == 0 else str(number)
            print(string_number)

            self.sudoku_board.itemconfig(self.numbers[self.selected_row][self.selected_column][1], text=string_number)
            self.sudoku_numbers[self.selected_row][self.selected_column] = number

    def select_field(self, event):
        column = int(event.x / self.set_width(1 / 18))
        row = int(event.y / self.set_width(1 / 18))


        if not self.changeable_numbers[row][column]: return

        if self.selected_row is not None:
            self.sudoku_board.itemconfig(self.numbers[self.selected_row][self.selected_column][0], fill="white")

        self.selected_row = row
        self.selected_column = column

        self.sudoku_board.itemconfig(self.numbers[row][column][0], fill="#f0f1f5")

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
        self.sudoku_board.config(width=scale2w, height=self.set_height(0.75))

        self.sudoku_board.place(x=scale4w, y=0)
        self.number_buttons_frame.place(x=scale4w, y=self.set_height(0.8))
        self.help_buttons_frame.place(x=scale4w, y=self.set_height(0.9))
        self.info_frame.place(x=self.set_width(0.8), y=0)
        self.main_buttons_frame.place(x=0, y=0)

        for index, button in enumerate(self.main_buttons):
            button.place(x=0, y=index * self.set_height(0.065), width=scale5w)
            button.config(font=Font(family="Open Sans", size=self.font_size))

        for index, button in enumerate(self.help_buttons):
            button.place(x=index * self.set_height(1 / 6), y=0, width=scale5w)
            button.config(font=Font(family="Open Sans", size=self.font_size))

        for button in self.number_buttons:
            button.config(font=Font(family="Open Sans", size=self.font_size))

        for index, line in enumerate(self.vertical_lines):
            self.sudoku_board.coords(line, (index + 1) * scale18w, 0, (index + 1) * scale18w, scale2w)

        for index, line in enumerate(self.horizontal_lines):
            self.sudoku_board.coords(line, 0, (index + 1) * scale18w, scale2w, (index + 1) * scale18w)

        for row, line in enumerate(self.numbers):
            for column, field in enumerate(line):
                self.sudoku_board.coords(field[0], column * scale18w, row * scale18w,
                                         column * scale18w + scale18w, row * scale18w + scale18w)
                self.sudoku_board.coords(field[1], column * scale18w + scale36w, row * scale18w + scale36w)
                self.sudoku_board.itemconfig(self.numbers[row][column][1],
                                             font=Font(family="Open Sans", size=self.set_font(3 / 2)))


state = State()


# main #############################################


def main():
    state.app.title('Sudoku solver!')
    state.app.geometry(str(state.window_size_width) + "x" + str(state.window_size_height))

    state.set_changeable_numbers()

    state.sudoku_board.bind("<Button-1>", state.select_field)
    state.set_initial_sudoku_board()

    state.set_number_buttons()
    state.set_help_buttons()
    state.set_main_buttons()

    state.place()

    while True:
        state.app.update()
        if state.window_size_width != state.app.winfo_width() or state.window_size_height != state.window_size_height:
            if state.app.winfo_width() * 2 / 3 > state.app.winfo_height():
                state.window_size_width = int(state.app.winfo_height()*3/2)
                state.window_size_height = state.app.winfo_height()
            else:
                state.window_size_width = state.app.winfo_width()
                state.window_size_height = int(state.app.winfo_width() * 2/3)

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
