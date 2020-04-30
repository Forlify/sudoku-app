import tkinter as tk
import datetime
from threading import Timer as Time
import src.utils.utils as utils


class Timer():
    def __init__(self, app):
        self.root = app
        self.label = tk.Label(text="")
        self.label.pack()
        self.label.place(relx=0.77, rely=0.1, anchor='sw')
        self.time = utils.start_time.time()
        self.update_clock()
        timer = Time(1000, lambda: self.update_clock())
        timer.start()

    def update_clock(self):
        self.time = utils.addSecs(self.time)
        self.label.configure(text=self.time, font=utils.normal_font)
        self.root.after(1000, self.update_clock)
