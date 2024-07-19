import tkinter as tk
from tkinter import ttk
# import os
# import idlelib.idle
from tkinter import tix

root = tix.Tk()
root.tk.eval('package require Tix')
termf = tk.Frame(root, height=400, width=500)
pywindow = tix.Tk( screenName="pywindow")
# pywindow.pack()
# termf.pack(fill=BOTH, expand=YES)

# wid = termf.winfo_id()

# root.mainloop()

     
# def is_convertible_to_integer( input_str):
#     try:
#         int(input_str)
#         return True
#     except:
#         return False
    

# usrint = str(-15)
# print(int(usrint))
# print(type(usrint))
# print(is_convertible_to_integer(usrint))

# from tkinter import *
# import subprocess as sub

# p = sub.Popen('cmd.exe', stdout=sub.PIPE, stderr=sub.PIPE)
# output, errors = p.communicate()

# root = Tk()
# text = Text(root)
# text.pack()
# text.insert(END, output)
# root.mainloop()
