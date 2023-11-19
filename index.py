#!/usr/bin/python3

import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import random
import os

class Game(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.peoples = self.listPeople("pics")
        self.create_widgets()

    @staticmethod
    def listPeople(path: str):
        # List all student
        peoples = os.listdir("pics")
        peoples.remove(".gitkeep")
        return peoples

    def create_widgets(self):

        root.title("Who are you")

        self.correct_person = 0

        # create a label at center of window with image
        self.myimage = ttk.Label(root)
        self.myimage.grid(row=0, column=0, columnspan=3)

        # Create 3 text variable to store the name
        self.name1 = tk.StringVar()
        self.name2 = tk.StringVar()
        self.name3 = tk.StringVar()

        # Create button
        button1 = ttk.Button(root, width=30)
        button2 = ttk.Button(root, width=30)
        button3 = ttk.Button(root, width=30)

        self.on_click(0)

        # Create 3 button to guess the correct name

        button1["textvariable"] = self.name1
        button1["command"] = lambda: self.on_click(0)
        button1.grid(row=1, column=0, padx=10, pady=10)

        button2["textvariable"] = self.name2
        button2["command"] = lambda: self.on_click(1)
        button2.grid(row=1, column=1, padx=10, pady=10)

        button3["textvariable"] = self.name3
        button3["command"] = lambda: self.on_click(2)
        button3.grid(row=1, column=2, padx=10, pady=10)

    def on_click(self, choice: str):
        if (choice == self.correct_person):
            print("Correct")
        else:
            print("Wrong")
            return
        self.correct_person = random.randint(0, 2)
        names = [random.choice(self.peoples),random.choice(self.peoples),random.choice(self.peoples)]
        self.name1.set(names[0])
        self.name2.set(names[1])
        self.name3.set(names[2])
        global imgobj
        imgobj = ImageTk.PhotoImage(Image.open("pics/" + names[self.correct_person]))
        self.myimage["image"] = imgobj


root = tk.Tk()
myapp = Game(root)
myapp.mainloop()
