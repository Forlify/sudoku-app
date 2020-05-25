import tkinter as tk
import src.utils.utils as utils
from PIL import Image, ImageTk


class Timer:
    def __init__(self, app, frame):
        self.root = app
        self.frame = frame
        self.running = False
        self.time = utils.start_time.time()
        self.label = tk.Label(frame, text=self.time, font=utils.normal_font, fg=utils.orange,
                              background=utils.dark_blue)
        self.label.place(x=utils.set_width(1 / 50), y=utils.set_height(1 / 80))

        self.timer_img_unscaled = Image.open("img/timer.png")
        self.timer_img = ImageTk.PhotoImage(self.timer_img_unscaled.resize(
            (utils.set_width(0.018), utils.set_height(0.031)), Image.ANTIALIAS))
        self.timer = tk.Label(frame, background=utils.dark_blue, image=self.timer_img)
        self.timer.place(x=0, y=utils.set_height(1 / 40))

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
        self.label.place(x=utils.set_width(1 / 50), y=utils.set_height(1 / 80))

        self.timer_img = ImageTk.PhotoImage(self.timer_img_unscaled.resize(
            (utils.set_width(0.018), utils.set_height(0.031)), Image.ANTIALIAS))
        self.timer.config(image=self.timer_img)
        self.timer.place(x=0, y=utils.set_height(1 / 40))

    def reset(self):
        self.time = utils.start_time.time()

    def set_on(self):
        self.running = True
