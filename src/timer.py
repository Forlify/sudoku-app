import tkinter as tk
import src.utils.utils as utils


class Timer:
    def __init__(self, app, frame):
        self.root = app
        self.frame = frame
        self.running = False
        self.time = utils.start_time.time()
        self.label = tk.Label(frame, text=self.time, font=utils.normal_font, fg=utils.orange, background=utils.dark_blue)
        self.label.place(x=utils.set_width(1 / 80), y=utils.set_height(1/80))
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
        self.label.place(x=utils.set_width(1 / 80), y=utils.set_height(1/80))

    def reset(self):
        self.time = utils.start_time.time()

    def set_on(self):
        self.running = True



