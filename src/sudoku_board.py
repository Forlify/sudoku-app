from src.sudoku import Sudoku
from time import time
from tkinter import *
from tkinter import Canvas, messagebox
from tkinter import filedialog
from src.highscores import HighScores
import src.utils.utils as utils
from src.photo_camera_read import read_image, read_camera
from src.timer import Timer


class SudokuBoard:
    def __init__(self, state, initial_sudoku):
        self.state = state
        self.sudoku_board = Canvas(state.app, width=utils.set_width(1 / 2), height=utils.set_height(0.75), bd=0,
                                   highlightbackground="black", highlightthickness=5)
        self.sudoku_board.bind("<Button-1>", state.select_field)

        self.horizontal_lines = []
        self.vertical_lines = []
        self.sudoku = Sudoku(initial_sudoku)
        self.numbers = []
        self.start_time = time()
        self.scores = HighScores()

    def set_initial_sudoku_board(self, scale36, scale18, scale2, bigger_font):
        for row, line in enumerate(self.sudoku.sudoku_numbers):
            numbers_in_row = []
            for column, number in enumerate(line):
                string_number = str(number) if number in self.sudoku.possible_values else " "
                string_color = utils.black if number in self.sudoku.possible_values else utils.dark_gray
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
                self.sudoku_board.create_line(0, 0, 0, 0, fill="black", width=(5 if index % 3 == 0 else 2)))
            self.horizontal_lines.append(
                self.sudoku_board.create_line(0, 0, 0, 0, fill="black", width=(5 if index % 3 == 0 else 2)))

    def change_sudoku(self, new_sudoku_numbers):
        self.state.sudoku_board.change_board(new_sudoku_numbers)

    def import_sudoku_from_file(self):
        source_file = filedialog.askopenfilename(initialdir="./sudoku-files", title="Select File",
                                                 filetypes=(("text", ".txt"), ("all files", "*.*")))
        with open(source_file) as text_file:
            sudoku_numbers = [list(map(int, line.split())) for line in text_file]
        self.change_sudoku(sudoku_numbers)

    def import_sudoku_from_image(self):
        source_file = filedialog.askopenfilename(initialdir="./img", title="Select File",
                                                 filetypes=(("text", ".png"), ("all files", "*.*")))
        sudoku_numbers = read_image(source_file)
        self.change_sudoku(sudoku_numbers)

    def import_sudoku_from_camera(self):
        sudoku_numbers = read_camera()
        self.change_sudoku(sudoku_numbers)

    def import_sudoku(self):
        import_window = Toplevel()
        import_window.focus_set()
        import_window.grab_set()
        import_window.title('Import source:')
        message = "Choose import source:"
        Label(import_window, text=message).pack()
        Button(import_window, text='Camera', command=lambda: self.import_sudoku_from_camera()).pack()
        Button(import_window, text='Photo', command=lambda: self.import_sudoku_from_image()).pack()
        Button(import_window, text='File', command=lambda: self.import_sudoku_from_file()).pack()

    def get_hint(self):
        hint = self.sudoku.get_hint()
        if hint:
            x, y, value = hint
            self.sudoku.change_value(x, y, value)
            self.sudoku_board.itemconfig(self.numbers[x][y][1], text=str(value))

    def check(self):
        check = self.sudoku.check_sudoku()
        if check == "all":
            end_time = time()
            score = round(end_time - self.start_time, 1)
            self.scores.add_score(score)
            messagebox.showinfo("Congratulation!", "You've completed sudoku in: " + str(score) + " s!")
        elif check == "ok":
            messagebox.showinfo(":)", "Keep going, everything is ok right now..")
        else:
            messagebox.showinfo(":(", "Not ok.")

    def fill_board(self):
        for x in range(9):
            for y in range(9):
                value = self.sudoku.sudoku_numbers[x][y]
                string_color = utils.black if value in self.sudoku.possible_values else utils.dark_gray
                string_value = value if value else " "
                self.sudoku_board.itemconfig(
                    self.numbers[x][y][1], text=string_value, fill=string_color)

    def reset_board(self):
        self.start_time = time()
        self.sudoku.reset_sudoku()
        self.fill_board()

    def change_board(self, new_sudoku_numbers):
        self.start_time = time()
        self.sudoku = Sudoku(new_sudoku_numbers)
        self.fill_board()
        # Reset timer:
        self.state.timer = Timer(self.state.app)

    def get_scores(self):
        self.scores.show_scores()
