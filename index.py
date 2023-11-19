#!/usr/bin/python3

from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import random
import os

# List all student
students = os.listdir("pics")
students.remove(".gitkeep")

root = Tk()
root.title("Feet to Meters")

correct_student = 0


# create a label at center of window with image
myimage = ttk.Label(root)
myimage.grid(row=0, column=0, columnspan=3)

# Create 3 text variable to store the name
name1 = StringVar()
name2 = StringVar()
name3 = StringVar()

# Create button
button1 = ttk.Button(root, width=30)
button2 = ttk.Button(root, width=30)
button3 = ttk.Button(root, width=30)

def on_click(choice: str):
    global correct_student
    if (choice == correct_student):
        print("Correct")
    else:
        print("Wrong")
        return
    correct_student = random.randint(0, 2)
    names = [random.choice(students),random.choice(students),random.choice(students)]
    name1.set(names[0])
    name2.set(names[1])
    name3.set(names[2])
    global imgobj
    imgobj = ImageTk.PhotoImage(Image.open("pics/" + names[correct_student]))
    myimage["image"] = imgobj

on_click(0)

# Create 3 button to guess the correct name

button1["textvariable"] = name1
button1["command"] = lambda: on_click(0)
button1.grid(row=1, column=0, padx=10, pady=10)

button2["textvariable"] = name2
button2["command"] = lambda: on_click(1)
button2.grid(row=1, column=1, padx=10, pady=10)

button3["textvariable"] = name3
button3["command"] = lambda: on_click(2)
button3.grid(row=1, column=2, padx=10, pady=10)


root.mainloop()