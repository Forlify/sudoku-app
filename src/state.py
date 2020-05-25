from tkinter import *
from tkinter.font import Font
from src.sudoku_board import SudokuBoard
import src.utils.utils as utils
from src.timer import Timer
from PIL import Image, ImageTk


class State:
    def __init__(self, initial_sudoku_numbers):
        self.app = utils.app
        self.selected_field = (None, None)
        self.sudoku_board = SudokuBoard(self, initial_sudoku_numbers)
        self.number_buttons = []
        self.help_buttons = []
        self.main_buttons = []
        self.number_buttons_frame = Frame(self.app, background=utils.dark_blue)
        self.help_buttons_frame = Frame(self.app, background=utils.dark_blue)
        self.main_buttons_frame = Frame(self.app, background=utils.dark_blue)
        self.info_frame = Frame(self.app, background=utils.dark_blue)

        self.main_buttons_unscaled = [
            Image.open("img/quit-btn.png"),
            Image.open("img/reset-btn.png"),
            Image.open("img/high-scores-btn.png"),
            Image.open("img/import-btn.png")]
        self.main_buttons_img = [None] * 4

        self.help_buttons_unscaled = [
            Image.open("img/hint-btn.png"),
            Image.open("img/check-btn.png")]
        self.help_buttons_img = [None] * 2

        self.number_buttons_unscaled = [
            Image.open("img/x-btn.png"),
            Image.open("img/1-btn.png"),
            Image.open("img/2-btn.png"),
            Image.open("img/3-btn.png"),
            Image.open("img/4-btn.png"),
            Image.open("img/5-btn.png"),
            Image.open("img/6-btn.png"),
            Image.open("img/7-btn.png"),
            Image.open("img/8-btn.png"),
            Image.open("img/9-btn.png")]
        self.number_buttons_img = [None] * 10

        self.app.title('SudokuApp')
        self.app.iconbitmap('img/sudoku.ico')
        self.app.geometry(str(utils.window_width) + "x" + str(utils.window_height))
        self.set_initial_sudoku_board()
        self.set_number_buttons()
        self.set_help_buttons()
        self.set_main_buttons()
        self.place(True)
        self.timer = Timer(self.app, self.info_frame)

    def set_initial_sudoku_board(self):
        scale36 = utils.set_width(1 / 36)
        scale18 = utils.set_width(1 / 18)
        scale2 = utils.set_width(1 / 2)
        self.sudoku_board.set_initial_sudoku_board(scale36, scale18, scale2, utils.bigger_font)

    def actualize_font(self):
        utils.font_size = utils.set_height(1 / 25)
        utils.normal_font = Font(family="Open Sans", size=utils.font_size)
        utils.bigger_font = Font(family="Open Sans", size=utils.set_font(3 / 2))

    def set_number_buttons(self):
        for index in range(10):
            self.number_buttons.append(Label(self.number_buttons_frame, background=utils.dark_blue))
            self.number_buttons[index].bind("<Button-1>", lambda event, num=index: self.set_sudoku_number(event, num))

    def set_help_buttons(self):
        label = Label(self.help_buttons_frame, background=utils.dark_blue)
        label.bind("<Button-1>", lambda e: self.sudoku_board.get_hint())
        self.help_buttons.append(label)

        label = Label(self.help_buttons_frame, background=utils.dark_blue)
        label.bind("<Button-1>", lambda e: self.sudoku_board.check())
        self.help_buttons.append(label)

    def set_main_buttons(self):
        label = Label(self.main_buttons_frame, background=utils.dark_blue)
        label.bind("<Button-1>", lambda e: self.app.destroy())
        self.main_buttons.append(label)

        label = Label(self.main_buttons_frame, background=utils.dark_blue)
        label.bind("<Button-1>", lambda e: self.sudoku_board.reset_board())
        self.main_buttons.append(label)

        label = Label(self.main_buttons_frame, background=utils.dark_blue)
        label.bind("<Button-1>", lambda e: self.sudoku_board.get_scores())
        self.main_buttons.append(label)

        label = Label(self.main_buttons_frame, background=utils.dark_blue)
        label.bind("<Button-1>", lambda e: self.sudoku_board.import_sudoku())
        self.main_buttons.append(label)

    def set_sudoku_number(self, event, number):
        row = self.selected_field[0]
        column = self.selected_field[1]

        if row is not None and self.sudoku_board.sudoku.changeable_numbers[row][column]:
            string_number = "  " if number == 0 else str(number)

            self.sudoku_board.sudoku_board.itemconfig(self.sudoku_board.numbers[row][column][1], text=string_number)
            self.sudoku_board.change_value(row, column, number)

    def select_field(self, event):
        column = int(event.x / utils.set_width(1 / 18))
        row = int(event.y / utils.set_width(1 / 18))

        if not self.sudoku_board.sudoku.changeable_numbers[row][column]: return

        if self.selected_field[0] is not None:
            self.sudoku_board.sudoku_board.itemconfig(
                self.sudoku_board.numbers[self.selected_field[0]][self.selected_field[1]][0], fill=utils.blue)

        self.selected_field = (row, column)

        self.sudoku_board.sudoku_board.itemconfig(self.sudoku_board.numbers[row][column][0], fill=utils.dark_blue)

    def place(self, first=False):
        scale2w = utils.set_width(1 / 2)
        scale4w = utils.set_width(1 / 4)
        scale5w = utils.set_width(1 / 5)

        scale18w = utils.set_width(1 / 18)
        scale36w = utils.set_width(1 / 36)
        scale2h = utils.set_height(1 / 2)

        self.number_buttons_frame.config(width=scale2w, height=scale2h)
        self.help_buttons_frame.config(width=scale2w, height=scale2h)
        self.main_buttons_frame.config(width=scale5w, height=utils.window_height)
        self.info_frame.config(width=scale5w, height=utils.window_height)
        self.sudoku_board.sudoku_board.config(width=scale2w - 10, height=utils.set_height(0.75) - 10)

        self.sudoku_board.sudoku_board.place(x=scale4w, y=utils.set_height(1 / 36))
        self.number_buttons_frame.place(x=scale4w, y=utils.set_height(0.8))
        self.help_buttons_frame.place(x=scale4w, y=utils.set_height(0.9))
        self.info_frame.place(x=utils.set_width(0.8), y=0)
        self.main_buttons_frame.place(x=utils.set_width(1 / 40), y=utils.set_height(1 / 36))

        self.help_buttons_img[0] = ImageTk.PhotoImage(self.help_buttons_unscaled[0].resize(
            (int(scale2w * 0.39), utils.set_height(0.08)), Image.ANTIALIAS))
        self.help_buttons_img[1] = ImageTk.PhotoImage(self.help_buttons_unscaled[1].resize(
            (int(scale2w * 0.59), utils.set_height(0.08)), Image.ANTIALIAS))

        self.help_buttons[0].config(image=self.help_buttons_img[0])
        self.help_buttons[1].config(image=self.help_buttons_img[1])

        self.help_buttons[0].place(x=4, y=0, width=int(scale2w * 0.39))
        self.help_buttons[1].place(x=4 + int(scale2w * 0.40), y=0, width=int(scale2w * 0.59))

        for index, button in enumerate(self.main_buttons):
            self.main_buttons_img[index] = ImageTk.PhotoImage(self.main_buttons_unscaled[index].resize(
                (scale5w, utils.set_height(0.078)), Image.ANTIALIAS))
            self.main_buttons[index].config(image=self.main_buttons_img[index])
            button.place(x=0, y=index * utils.set_height(0.094), width=scale5w)

        for index, button in enumerate(self.number_buttons):
            self.number_buttons_img[index] = ImageTk.PhotoImage(self.number_buttons_unscaled[index].resize(
                (int(scale2w / 11), utils.set_height(0.08)), Image.ANTIALIAS))
            self.number_buttons[index].config(image=self.number_buttons_img[index])
            button.place(x=index * scale2w / 10, y=0)

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
        if not first:
            self.timer.update_size()
# 1.165
