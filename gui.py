from tkinter import *
from tkinter.font import Font

# configuration ####################################


class State:

    def __init__(self):
        self.app = Tk()

        self.selected_row = None
        self.selected_column = None

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

        self.number_buttons_frame = Frame(self.app, width=903, height=70)
        self.help_buttons_frame = Frame(self.app, width=903, height=70)
        self.main_buttons_frame = Frame(self.app, width=300, height=900, bg="#f0f1f5")
        self.info_frame = Frame(self.app, width=300, height=900, bg="#f0f1f5")
        self.sudoku_frame = Frame(self.app, width=902, height=902)
        self.sudoku_board = Canvas(self.sudoku_frame, width=900, height=900)

    def set_changable_numbers(self):
        for row in self.sudoku_numbers:
            row_changeable_numbers = []

            for number in row:
                row_changeable_numbers.append(number == 0)

            self.changeable_numbers.append(row_changeable_numbers)

    def set_initial_sudoku_numbers(self):
        for row, line in enumerate(self.initial_sudoku_numbers):
            numbers_in_row = []
            for column, number in enumerate(line):
                string_number = "  " if number == 0 else str(number)
                string_color = "#636e72" if number == 0 else "#2d3436"

                background = self.sudoku_board.create_rectangle(column * 100, row * 100,
                                                                column * 100 + 100, row * 100 + 100,
                                                                fill="white")

                text = self.sudoku_board.create_text(column * 100 + 50, row * 100 + 50,
                                                     text=string_number,
                                                     font=Font(family="Open Sans", size=60),
                                                     fill=string_color)

                numbers_in_row.append([background, text])

            self.numbers.append(numbers_in_row)

    def set_number_buttons(self):
        for index in range(10):
            self.number_buttons.append(Button(self.number_buttons_frame,
                                              text="NONE" if index == 0 else index,
                                              font=Font(family="Open Sans", size=40),
                                              padx=26))
            self.number_buttons[index].bind("<Button-1>",
                                            lambda event, number=index: self.set_sudoku_number(event, number))
            self.number_buttons[index].pack(side=LEFT)

    def set_help_buttons(self):
        self.help_buttons.append(Button(self.help_buttons_frame,
                                        text="HINT",
                                        font=Font(family="Open Sans", size=40)))

        self.help_buttons.append(Button(self.help_buttons_frame,
                                        text="CHECK",
                                        font=Font(family="Open Sans", size=40)))

        self.help_buttons.append(Button(self.help_buttons_frame,
                                        text="SOMETHING",
                                        font=Font(family="Open Sans", size=40)))

        for index, button in enumerate(self.help_buttons):
            button.place(x=index*300, y=0, width=300)

    def set_main_buttons(self):
        self.main_buttons.append(Button(self.main_buttons_frame,
                                        text="IMPORT",
                                        font=Font(family="Open Sans", size=40)))

        self.main_buttons.append(Button(self.main_buttons_frame,
                                        text="RESET",
                                        font=Font(family="Open Sans", size=40)))

        self.main_buttons.append(Button(self.main_buttons_frame,
                                        text="HIGH SCORES",
                                        font=Font(family="Open Sans", size=40)))

        for index, button in enumerate(self.main_buttons):
            button.place(x=0, y=index*70, width=300)

    def set_sudoku_number(self, event, number):
        if self.selected_row and self.changeable_numbers[self.selected_row][self.selected_column]:
            string_number = "  " if number == 0 else str(number)

            self.sudoku_board.itemconfig(self.numbers[self.selected_row][self.selected_column][1], text=string_number)
            self.sudoku_numbers[self.selected_row][self.selected_column] = number;

    def select_field(self, event):
        column = int(event.x / 100)
        row = int(event.y / 100)

        if not self.changeable_numbers[row][column]: return;

        if self.selected_row is not None:
            self.sudoku_board.itemconfig(self.numbers[self.selected_row][self.selected_column][0], fill="white")

        self.selected_row = row
        self.selected_column = column

        self.sudoku_board.itemconfig(self.numbers[row][column][0], fill="#f0f1f5")

    def render_sudoku_board(self):
        for i in range(10):
            self.sudoku_board.create_line(i * 100 + 2, 0, i * 100 + 2, 900, fill="black",
                                           width=(5 if i % 3 == 0 else 2))
            self.sudoku_board.create_line(0, i * 100 + 2, 900, i * 100 + 2, fill="black",
                                           width=(5 if i % 3 == 0 else 2))


state = State()
# main #############################################

def main():
    state.app.title('Sudoku solver!')
    state.app.geometry('1700x1080')

    state.set_changable_numbers()

    state.sudoku_frame.place(x=400, y=50)
    state.sudoku_board.place(x=0, y=0)
    state.sudoku_board.bind("<Button-1>", state.select_field)
    state.set_initial_sudoku_numbers()
    state.render_sudoku_board()

    state.number_buttons_frame.place(x=402, y=953)
    state.set_number_buttons()

    state.help_buttons_frame.place(x=402, y=1016)
    state.set_help_buttons()

    state.main_buttons_frame.place(x=50, y=53)
    state.set_main_buttons()

    state.info_frame.place(x=1350, y=53)
    state.app.mainloop()


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
#  [3, 4, 5, 2, 8, 6, 1, 7, 9]]