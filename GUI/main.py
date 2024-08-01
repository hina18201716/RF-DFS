import tkinter as tk
from tkinter import ttk
from tkinter.ttk import *
from functions import *
import sys


root = tk.Tk()
DFSwindow = FrontEnd(root)


# stdout will be printed in textbox 
console = tk.Text( root, height = 10, width = 50)
console.pack()
consoleButton = tk.Button(root, text = 'output', command = lambda : print("here is stdout") )
consoleButton.pack()   

def redirector(inputStr):
    console.insert(INSERT, inputStr)

sys.stdout.write = redirector #whenever sys.stdout.write is called, redirector is called.


root.mainloop()