from tkinter import messagebox


class HighScores:
    def __init__(self):
        self.scores_number = 10
        self.scores = self.read_scores()

    def add_score(self, score):
        self.scores = self.read_scores()
        if len(self.scores) == self.scores_number:
            self.scores.append(score)
            self.scores.sort()
            self.scores = self.scores[:-1]
        else:
            self.scores.append(score)
            self.scores.sort()
        self.update_scores()

    def show_scores(self):
        string_result = "Your high scores: \n"
        for index, score in enumerate(self.scores):
            string_result = string_result + str(index + 1) + ". " + str(score) + " s \n"
        messagebox.showinfo("Scores: ", string_result)

    def update_scores(self):
        with open('score.txt', "w") as write_score:
            for index, item in enumerate(self.scores):
                if index == len(self.scores) - 1:
                    write_score.write(str(item))
                else:
                    write_score.write(str(item) + ' ')
        write_score.close

    def read_scores(self):
        with open('score.txt', "r") as read_score:
            scores = read_score.read()
            scores = scores.split(' ')
            scores = list(map(float, scores))
        return scores
