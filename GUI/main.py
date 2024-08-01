import tkinter as tk
from tkinter import ttk
from tkinter.ttk import *
from functions import *
import sys


root = tk.Tk()
DFSwindow = FrontEnd(root)


# python  console creation
console = tk.Text(root, height = 10 )
console.pack()
consoleButton = tk.Button(root, text = 'output', command = lambda : print("here is stdout") )
consoleButton.pack()   

def redirector(inputStr):
    console.insert(INSERT, inputStr)

sys.stdout.write = redirector #whenever sys.stdout.write is called, redirector is called.


root.mainloop()