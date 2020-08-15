import xml.etree.ElementTree as ET
from tkinter import *
from tkinter import ttk
from tkinter import filedialog


class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.title("Python Tkinter Dialog Widget")
        self.minsize(640, 100)

        self.labelFrame = ttk.LabelFrame(self, text="Open File")
        self.labelFrame.grid(column=1, row=1, padx=20, pady=20)

        self.fileNameLabel = ttk.Label(self.labelFrame, text="")
        self.fileNameLabel.grid(column=1, row=2)

        self.SubmitBtn = ttk.Button(self.labelFrame, text="Submit", command=self.submit)
        self.SubmitBtn.grid(row=3, column=1, sticky='S', padx=5, pady=2)

        self.button = ttk.Button(self.labelFrame, text="Browse A File", command=self.fileDialog)
        self.button.grid(column=1, row=1)

        self.fileName = None

    def fileDialog(self):
        self.filename = filedialog.askopenfilename(initialdir="/", title="Select A File", filetype=(("jpeg files", "*.jpg"), ("all files", "*.*")))
        self.fileNameLabel.configure(text=self.filename)

    def submit(self):
        self.fileName = self.fileNameLabel['text']
        self.destroy()