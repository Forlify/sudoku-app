from tkinter.font import Font
from tkinter import *
import datetime

app = Tk()
window_width = 1500
window_height = 1000
light_gray = "#f0f1f5"
dark_gray = "#636e72"
black = "#2d3436"
font_size = int(window_height / 25)
normal_font = Font(family="Open Sans", size=font_size)
bigger_font = Font(family="Open Sans", size=int(font_size * 3 / 2))

def set_width(scale):
    return int(window_width * scale)

def set_height(scale):
    return int(window_height * scale)

def set_font(scale):
    return int(font_size * scale)

start_time = datetime.datetime(100,1,1,23,59,59)

def addSecs(tm, secs=1):
    full_date = datetime.datetime(100, 1, 1, tm.hour, tm.minute, tm.second)
    full_date = full_date + datetime.timedelta(seconds=secs)
    return full_date.time()