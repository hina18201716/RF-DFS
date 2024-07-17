# from tkinter import *
# import os

# root = Tk()
# termf = Frame(root, height=400, width=500)


# # wid = termf.winfo_id()
# os.system('start cmd -into %d -geometry 20x20 -sb &' % termf.winfo_id())
# # os.system("python %d -geometry 40x20 -sb &" % wid)


# termf.pack(fill=BOTH, expand=YES)
# root.mainloop()

     
def is_convertible_to_integer( input_str):
    try:
        int(input_str)
        return True
    except:
        return False
    

usrint = str(-15)
print(int(usrint))
print(type(usrint))
print(is_convertible_to_integer(usrint))