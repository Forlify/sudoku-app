from src.sudoku import Sudoku
from time import time
from tkinter import *
from tkinter import Canvas, messagebox
from tkinter import filedialog
from src.highscores import HighScores
import src.utils.utils as utils
from src.photo_camera_read import read_image, read_camera
from PIL import Image, ImageTk


class SudokuBoard:
    def __init__(self, state, initial_sudoku):
        self.state = state
        self.sudoku_board = Canvas(state.app, width=utils.set_width(1 / 2), height=utils.set_height(0.75), bd=0,
                                   highlightbackground=utils.white, highlightthickness=5)
        self.sudoku_board.bind("<Button-1>", state.select_field)

        self.horizontal_lines = []
        self.vertical_lines = []
        self.sudoku = Sudoku(initial_sudoku)
        self.numbers = []
        self.start_time = time()
        self.scores = HighScores()
        self.solved = False

        self.button_images = [
            ImageTk.PhotoImage(Image.open("img/random-btn.png")),
            ImageTk.PhotoImage(Image.open("img/file-btn.png")),
            ImageTk.PhotoImage(Image.open("img/camera-btn.png")),
            ImageTk.PhotoImage(Image.open("img/photo-btn.png"))
        ]

    def set_initial_sudoku_board(self, scale36, scale18, scale2, bigger_font):
        for row, line in enumerate(self.sudoku.sudoku_numbers):
            numbers_in_row = []
            for column, number in enumerate(line):
                string_number = str(number) if number in self.sudoku.possible_values else " "
                string_color = utils.white if number in self.sudoku.possible_values else utils.white
                background = self.sudoku_board.create_rectangle(column * scale18, row * scale18,
                                                                column * scale18 + scale18, row * scale18 + scale18,
                                                                fill=utils.blue, outline=utils.blue)

                text = self.sudoku_board.create_text(column * scale18 + scale36, row * scale18 + scale36,
                                                     text=string_number, fill=string_color,
                                                     font=bigger_font)

                numbers_in_row.append([background, text])
            self.numbers.append(numbers_in_row)

        for index in range(1, 9):
            self.vertical_lines.append(
                self.sudoku_board.create_line(0, 0, 0, 0, fill=utils.white, width=(5 if index % 3 == 0 else 2)))
            self.horizontal_lines.append(
                self.sudoku_board.create_line(0, 0, 0, 0, fill=utils.white, width=(5 if index % 3 == 0 else 2)))

    def change_sudoku(self, new_sudoku_numbers):
        self.solved = False
        self.state.sudoku_board.change_board(new_sudoku_numbers)

    def random_sudoku(self, window):
        self.sudoku.generate_sudoku()
        self.change_sudoku(self.sudoku.sudoku_numbers)
        window.destroy()

    def import_sudoku_from_file(self, window):
        source_file = filedialog.askopenfilename(initialdir="./sudoku-files", title="Select File",
                                                 filetypes=(("text", ".txt"), ("all files", "*.*")))
        with open(source_file) as text_file:
            sudoku_numbers = [list(map(int, line.split())) for line in text_file]
        self.change_sudoku(sudoku_numbers)
        window.destroy()

    def import_sudoku_from_image(self, window):
        source_file = filedialog.askopenfilename(initialdir="./img", title="Select File",
                                                 filetypes=(("text", ".png"), ("all files", "*.*")))
        sudoku_numbers = read_image(source_file)
        self.change_sudoku(sudoku_numbers)
        window.destroy()

    def import_sudoku_from_camera(self, window):
        sudoku_numbers = read_camera()
        self.change_sudoku(sudoku_numbers)
        window.destroy()

    def import_sudoku(self):
        import_window = Toplevel(background=utils.dark_blue)
        import_window.geometry("320x200")
        import_window.focus_set()
        import_window.grab_set()
        import_window.title('Import source:')
        message = "Choose import source:"
        Label(import_window, text=message, fg=utils.white, background=utils.dark_blue).pack()

        label = Label(import_window, background=utils.dark_blue, image=self.button_images[0])
        label.bind("<Button-1>", lambda e: self.random_sudoku(import_window))
        label.place(x=20, y=20)

        label = Label(import_window, background=utils.dark_blue, image=self.button_images[1])
        label.bind("<Button-1>", lambda e: self.import_sudoku_from_file(import_window))
        label.place(x=165, y=20)

        label = Label(import_window, background=utils.dark_blue, image=self.button_images[2])
        label.bind("<Button-1>", lambda e: self.import_sudoku_from_camera(import_window))
        label.place(x=20, y=105)

        label = Label(import_window, background=utils.dark_blue, image=self.button_images[3])
        label.bind("<Button-1>", lambda e: self.import_sudoku_from_image(import_window))
        label.place(x=165, y=105)

    def check(self, on_click=True):
        if self.solved and on_click:
            messagebox.showinfo("Congratulation!", "You've already solved this sudoku!")
            return
        check = self.sudoku.check_sudoku()
        if check == "all":
            end_time = time()
            score = round(end_time - self.start_time, 1)
            self.state.timer.set_on_off()
            messagebox.showinfo("Congratulation!", "You've completed sudoku in: " + str(score) + " s!")
            self.solved = True
            self.scores.add_score(score, self.state)

        elif check == "ok" and on_click:
            messagebox.showinfo(":)", "Keep going, everything is ok right now..")
        elif on_click:
            messagebox.showinfo(":(", "Not ok.")

    def get_hint(self):
        hint = self.sudoku.get_hint()
        if hint:
            x, y, value = hint
            self.sudoku.change_value(x, y, value)
            self.sudoku_board.itemconfig(self.numbers[x][y][1], text=str(value))
        self.check(on_click=False)

    def fill_board(self):
        for x in range(9):
            for y in range(9):
                value = self.sudoku.sudoku_numbers[x][y]
                string_color = utils.orange if value in self.sudoku.possible_values else utils.white
                string_value = value if value else " "
                self.sudoku_board.itemconfig(self.numbers[x][y][1], text=string_value, fill=string_color)

    def reset_board(self):
        self.sudoku.reset_sudoku()
        self.fill_board()

    def change_board(self, new_sudoku_numbers):
        self.sudoku = Sudoku(new_sudoku_numbers)
        self.fill_board()
        # Reset timer:
        self.start_time = time()
        self.state.timer.reset()
        self.state.timer.set_on()

    def get_scores(self):
        self.scores.show_scores()

    def change_value(self, row, column, number):
        self.sudoku.change_value(row, column, number)
        self.check(on_click=False)
