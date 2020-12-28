from tkinter import filedialog
from tkinter import *
import tkinter as tk
import sys, os

# pyinstaller --onefile --clean -y --add-data="images\schwarz-logo.gif;images" GUI.py

root = Tk()
global logo

if getattr(sys, 'frozen', False):
    logo = PhotoImage(file=os.path.join(sys._MEIPASS, "images/schwarz-logo.gif"))
else:
    logo = PhotoImage(file="images/schwarz-logo.gif")

label_w3 = tk.StringVar()
label_w3.set("Enter Scorm file...")
w1 = Label(root, image=logo).pack(side="left")
explanation = """Offline Course Player (c) 2020 by Timo Piechotta
Choose a valid SCORM ZIP-Package"""
w2 = Label(root,
           justify=LEFT,
           padx = 10,
           text=explanation).pack(side="right")
w3 = Label(root,
           justify=LEFT,
           padx = 10,
           text=label_w3.get()).pack(side="top")

def helloCallBack():
    root.filename = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(("all files", "*.*"), ("all files", "*.*")))
    label_w3.set(root.filename)
    print(root.filename)

B = Button(root, text ="Hello", command = helloCallBack)
B.pack()

root.mainloop()