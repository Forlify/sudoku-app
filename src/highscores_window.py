from tkinter import *
from tkinter.ttk import *


class HighscoresWindow(Frame):

    def __init__(self, parent, scores):
        Frame.__init__(self, parent)
        self.CreateUI()
        self.LoadTable(scores)
        self.grid(sticky = (N,S,W,E))
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

    def CreateUI(self):
        tv = Treeview(self)
        tv['columns'] = ('name', 'score', 'date')
        tv.heading("#0", text='Index', anchor='w')
        tv.column("#0", anchor="w", width=100)
        tv.heading('name', text='Name')
        tv.column('name', anchor='center', width=100)
        tv.heading('score', text='Score')
        tv.column('score', anchor='center', width=100)
        tv.heading('date', text='Date')
        tv.column('date', anchor='center', width=100)
        tv.grid(sticky = (N,S,W,E))
        self.treeview = tv
        self.grid_rowconfigure(0, weight = 1)
        self.grid_columnconfigure(0, weight = 1)

    def LoadTable(self, scores):
        for index, [name, time, date] in enumerate(scores):
            self.treeview.insert('', 'end', text=str(index + 1), values=(name,
                                time, date))
