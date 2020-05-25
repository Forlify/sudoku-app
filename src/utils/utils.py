from tkinter.font import Font
from tkinter import *
import datetime

blue = "#4b5a6d"
light_blue = "#4b5a6d"
light_gray = "#f4f4f5" # do zmiany
orange = "#f89e72"
white = "#f4f4f5"
dark_blue = '#374956'

app = Tk()
app.configure(bg=dark_blue)
window_width = 1500
window_height = 1000

font_size = int(window_height / 25)
normal_font = Font(family="Open Sans", size=font_size)
bigger_font = Font(family="Open Sans", size=int(font_size * 3 / 2))

def set_width(scale):
    return int(window_width * scale)

def set_height(scale):
    return int(window_height * scale)

def set_font(scale):
    return int(font_size * scale)

start_time = datetime.datetime(100,1,1,0,0,0)

def addSecs(tm, secs=1):
    full_date = datetime.datetime(100, 1, 1, tm.hour, tm.minute, tm.second)
    full_date = full_date + datetime.timedelta(seconds=secs)
    return full_date.time()