import tkinter as tk
import src.utils.utils as utils


class Timer:
    def __init__(self, app):
        self.root = app
        self.running = False
        self.time = utils.start_time.time()
        self.label = tk.Label(text=self.time, font=utils.normal_font)
        self.label.pack()
        self.label.place(relx=0.77, rely=0.1, anchor='sw')
        self.update_clock()

    def update_clock(self):
        if self.running:
            self.time = utils.addSecs(self.time)
            self.label.configure(text=self.time, font=utils.normal_font)
        self.root.after(1000, self.update_clock)

    def set_on_off(self):
        self.running = not self.running

    def update_size(self):
        self.label.configure(text=self.time, font=utils.normal_font)

    def reset(self):
        self.time = utils.start_time.time()



