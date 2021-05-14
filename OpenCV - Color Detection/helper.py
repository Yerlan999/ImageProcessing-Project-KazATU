# explore the mouse wheel with the Tkinter GUI toolkit
# Windows and Linux generate different events
# tested with Python25
import tkinter as tk
from tkinter import *
import os

def test(*args):
    print(args)
    # print("Envoked!")

def mouse_wheel(event):
    pass

try:
    root = tk.Tk()

    root.geometry("1500x700")
    root.title('turn mouse wheel')
    root['bg'] = 'darkgreen'

    tk.Button(root, text="TestButton").place(x=1350, y=0)


    scroll = tk.Scrollbar(root, command=test)
    scroll.pack(side = RIGHT, fill = Y)


    # with Windows OS
    root.bind("<MouseWheel>", mouse_wheel)
    # with Linux OS
    root.bind("<Button-4>", mouse_wheel)
    root.bind("<Button-5>", mouse_wheel)
    root.mainloop()
finally:
    os.system("taskkill /F /IM python3.8.exe /T")
