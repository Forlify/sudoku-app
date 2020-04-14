from tkinter import messagebox

class HighScores:
    def __init__(self):
        self.scores_number = 10
        self.scores = []
    def add_score(self, score):
        if len(self.scores) == self.scores_number:
            self.scores.append(score)
            sorted(self.scores)
            self.scores = self.scores[:-1]
        else:
            self.scores.append(score)
            sorted(self.scores)
    def show_scores(self):
        string_result = "Your high scores: \n"
        for index,score in enumerate(self.scores):
            string_result = string_result + str(index + 1) + ". " + str(score) + " s \n"
        messagebox.showinfo("Scores: ", string_result)