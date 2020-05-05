from time import sleep
from tkinter import messagebox
from tkinter import *
from datetime import datetime

import pickle

from src.highscores_window import HighscoresWindow


class HighScores:
    def __init__(self):
        self.scores_number = 20
        self.scores = self.read_scores()
        self.name = None

    def add_score(self, score, state):
        top = Toplevel()
        Label(top, text="Enter your name:").pack()
        text_box = Text(top, height=1, width=10)
        text_box.pack()
        button_commit = Button(top, height=1, width=10, command=lambda: self.add_name_score(text_box, top, score),
                               text="Commit")
        button_commit.pack()

    def add_name_score(self, text_box, top, score):
        self.name = text_box.get("1.0", "end-1c")
        top.destroy()
        self.scores = self.read_scores()
        date = datetime.date(datetime.now())
        new_record = [self.name, score, date]
        if len(self.scores) == self.scores_number:
            self.scores.append(new_record)
            self.scores.sort(key=lambda record: record[1])
            self.scores = self.scores[:-1]
        else:
            self.scores.append(new_record)
            self.scores.sort(key=lambda record: record[1])
        self.update_scores()

    def show_scores(self):
        top = Toplevel()
        HighscoresWindow(top, self.scores)


    def update_scores(self):
        scores_file = open("final_scores", 'wb')
        pickle.dump(self.scores, scores_file)
        scores_file.close()

    def read_scores(self):
        scores_file = open("final_scores", 'rb')
        scores = pickle.load(scores_file)
        scores_file.close()
        return scores
