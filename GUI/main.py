import tkinter as tk
from tkinter import ttk
from tkinter.ttk import *
from functions import *
import sys


root = tk.Tk()
DFSwindow = FrontEnd(root)

# stdout will be printed in textbox 
stdoutFrame = tk.Frame( root )
stdoutFrame.pack()
console = tk.Text( stdoutFrame , height = 10, width = 50)
console.grid( row = 0, column = 0 )

def redirector(inputStr):
    console.insert(INSERT, inputStr)

sys.stdout.write = redirector #whenever sys.stdout.write is called, redirector is called.


root.mainloop()