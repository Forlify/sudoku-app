from tkinter import *
from tkinter import filedialog
from tkinter.font import Font
from src.sudoku_board import SudokuBoard
import src.utils.utils as utils


class State:
    def __init__(self, initial_sudoku_numbers):
        self.app = utils.app
        self.selected_field = (None, None)
        self.sudoku_board = SudokuBoard(self, initial_sudoku_numbers)
        self.number_buttons = []
        self.help_buttons = []
        self.main_buttons = []
        self.number_buttons_frame = Frame(self.app, width=utils.set_width(1 / 10), height=utils.set_height(1 / 2))
        self.help_buttons_frame = Frame(self.app, width=utils.set_width(1 / 10), height=utils.set_height(1 / 2))
        self.main_buttons_frame = Frame(self.app, width=utils.set_width(1 / 5), height=utils.window_height)
        self.info_frame = Frame(self.app, width=utils.set_width(1 / 5), height=utils.window_height)

    def initalize_app(self):
        self.app.title('Sudoku solver!')
        self.app.iconbitmap('sudoku.ico')
        self.app.geometry(str(utils.window_width) + "x" + str(utils.window_height))
        self.set_initial_sudoku_board()
        self.set_number_buttons()
        self.set_help_buttons()
        self.set_main_buttons()
        self.place()

    def set_initial_sudoku_board(self):
        scale36 = utils.set_width(1 / 36)
        scale18 = utils.set_width(1 / 18)
        scale2 = utils.set_width(1 / 2)
        self.sudoku_board.set_initial_sudoku_board(scale36, scale18, scale2, utils.bigger_font)

    def change_sudoku(self, new_sudoku_numbers):
        self.sudoku_board.change_board(new_sudoku_numbers)

    def reset_sudoku_board(self):
        self.sudoku_board.reset_board()

    def import_sudoku(self):
        import_window = Toplevel()
        import_window.title('Import source:')
        message = "Choose import source:"
        Label(import_window, text=message).pack()
        Button(import_window, text='Camera').pack()
        Button(import_window, text='File', command=lambda: self.import_sudoku_from_file()).pack()

    def import_sudoku_from_file(self):
        source_file = filedialog.askopenfilename(initialdir="/", title="Select File",
                                                 filetypes=(("text", ".txt"), ("all files", "*.*")))
        with open(source_file) as text_file:
            sudoku_numbers = [list(map(int, line.split())) for line in text_file]
        self.change_sudoku(sudoku_numbers)

    def actualize_font(self):
        utils.font_size = utils.set_height(1 / 25)
        utils.normal_font = Font(family="Open Sans", size=utils.font_size)
        utils.bigger_font = Font(family="Open Sans", size=utils.set_font(3 / 2))

    def set_number_buttons(self):
        for index in range(10):
            self.number_buttons.append(Button(self.number_buttons_frame, text="NONE" if index == 0 else index,
                                              font=utils.normal_font))
            self.number_buttons[index].bind("<Button-1>", lambda event, num=index: self.set_sudoku_number(event, num))
            self.number_buttons[index].pack(side=LEFT)

    def set_help_buttons(self):
        self.help_buttons.append(
            Button(self.help_buttons_frame, text="HINT", command=lambda: self.sudoku_board.get_hint(),
                   font=utils.normal_font))
        self.help_buttons.append(
            Button(self.help_buttons_frame, text="CHECK", command=lambda: self.sudoku_board.check(),
                   font=utils.normal_font))
        self.help_buttons.append(Button(self.help_buttons_frame, text="FIELD", font=utils.normal_font))

    def set_main_buttons(self):
        self.main_buttons.append(Button(self.main_buttons_frame, text="QUIT",
                                        command=self.app.destroy, font=utils.normal_font))
        self.main_buttons.append(Button(self.main_buttons_frame, text="RESET",
                                        command=lambda: self.reset_sudoku_board(), font=utils.normal_font))
        self.main_buttons.append(Button(self.main_buttons_frame, text="HIGH SCORES",
                                        command=lambda: self.sudoku_board.get_scores(), font=utils.normal_font))
        self.main_buttons.append(Button(self.main_buttons_frame, text="IMPORT",
                                        command=lambda: self.import_sudoku(), font=utils.normal_font))

    def set_sudoku_number(self, event, number):
        row = self.selected_field[0]
        column = self.selected_field[1]

        if row is not None and self.sudoku_board.sudoku.changeable_numbers[row][column]:
            string_number = "  " if number == 0 else str(number)

            self.sudoku_board.sudoku_board.itemconfig(self.sudoku_board.numbers[row][column][1], text=string_number)
            self.sudoku_board.sudoku.change_value(row, column, number)

    def select_field(self, event):
        column = int(event.x / utils.set_width(1 / 18))
        row = int(event.y / utils.set_width(1 / 18))

        if not self.sudoku_board.sudoku.changeable_numbers[row][column]: return

        if self.selected_field[0] is not None:
            self.sudoku_board.sudoku_board.itemconfig(
                self.sudoku_board.numbers[self.selected_field[0]][self.selected_field[1]][0], fill="white")

        self.selected_field = (row, column)

        self.sudoku_board.sudoku_board.itemconfig(self.sudoku_board.numbers[row][column][0], fill=utils.light_gray)

    def place(self):
        scale2w = utils.set_width(1 / 2)
        scale4w = utils.set_width(1 / 4)
        scale5w = utils.set_width(1 / 5)
        scale10w = utils.set_width(1 / 10)
        scale18w = utils.set_width(1 / 18)
        scale36w = utils.set_width(1 / 36)
        scale2h = utils.set_height(1 / 2)

        self.number_buttons_frame.config(width=scale10w, height=scale2h)
        self.help_buttons_frame.config(width=scale5w * 3, height=scale2h)
        self.main_buttons_frame.config(width=scale5w, height=utils.window_height)
        self.info_frame.config(width=scale5w, height=utils.window_height)
        self.sudoku_board.sudoku_board.config(width=scale2w, height=utils.set_height(0.75))

        self.sudoku_board.sudoku_board.place(x=scale4w, y=0)
        self.number_buttons_frame.place(x=scale4w, y=utils.set_height(0.8))
        self.help_buttons_frame.place(x=scale4w, y=utils.set_height(0.9))
        self.info_frame.place(x=utils.set_width(0.8), y=0)
        self.main_buttons_frame.place(x=0, y=0)

        for index, button in enumerate(self.main_buttons):
            button.place(x=0, y=index * utils.set_height(0.065), width=scale5w)
            button.config(font=utils.normal_font)

        for index, button in enumerate(self.help_buttons):
            button.place(x=index * utils.set_width(1 / 6), y=0, width=scale5w)
            button.config(font=utils.normal_font)

        for button in self.number_buttons:
            button.config(font=utils.normal_font)

        for index, line in enumerate(self.sudoku_board.vertical_lines):
            self.sudoku_board.sudoku_board.coords(line, (index + 1) * scale18w, 0, (index + 1) * scale18w, scale2w)

        for index, line in enumerate(self.sudoku_board.horizontal_lines):
            self.sudoku_board.sudoku_board.coords(line, 0, (index + 1) * scale18w, scale2w, (index + 1) * scale18w)

        for row, line in enumerate(self.sudoku_board.numbers):
            for column, field in enumerate(line):
                self.sudoku_board.sudoku_board.coords(field[0], column * scale18w, row * scale18w,
                                                      column * scale18w + scale18w, row * scale18w + scale18w)
                self.sudoku_board.sudoku_board.coords(field[1], column * scale18w + scale36w, row * scale18w + scale36w)
                self.sudoku_board.sudoku_board.itemconfig(self.sudoku_board.numbers[row][column][1],
                                                          font=utils.bigger_font)
