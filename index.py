#!/usr/bin/python3

import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import random
import os

class Game(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        root.title("Who are you")

        self.picsPath = "pics"
        self.peoples = self.listPeople(self.picsPath)
        self.createWidgets()
        self.changePerson()

        root.bind("<Key>", self.on_keyboard_event)

    @staticmethod
    def listPeople(path: str):
        # List all student
        peoples = os.listdir(path)
        try:
            peoples.remove(".gitkeep")
        except:
            pass
        return peoples

    def createButtons(self, row: int, column: int):
        self.textVariables = []
        self.buttons = []
        for y in range(row):
            for x in range(column):
                self.textVariables.append(tk.StringVar())
                button = ttk.Button(root, width=30)
                button["textvariable"] = self.textVariables[y * column + x]
                button.grid(row=y + 1, column=x, padx=10, pady=10)
                # Is there a better way to do this?
                button["command"] = lambda y=y, x=x: self.onClick(y * column + x)
                self.buttons.append(button)

    def createWidgets(self):
        # create a label at center of window with image
        self.imageLabel = ttk.Label(root)
        self.imageLabel.grid(row=0, column=0, columnspan=3)
        self.currentImage = None

        self.createButtons(3,3)

    def changePerson(self):
        names = random.sample(self.peoples, len(self.textVariables))
        self.correct_person = random.randint(0, len(self.textVariables) - 1)

        # Texts and enable buttons
        for i, textVar in enumerate(self.textVariables):
            textVar.set(".".join(names[i].split(".")[:-1]))
            self.buttons[i]["state"] = tk.NORMAL

        # Image
        if (self.currentImage is not None):
            self.currentImage.close()
        self.currentImage = Image.open(os.path.join(self.picsPath, names[self.correct_person]))
        self.imgobj = ImageTk.PhotoImage(self.currentImage)
        self.imageLabel["image"] = self.imgobj

    def on_keyboard_event(self, event):
        if not event.char.isnumeric() or event.char == "0":
            return
        choice = int(event.char)
        # Transform key pressed to correct index
        if choice < 4:
            choice += 6
        elif choice > 6:
            choice -=6
        # Index between 0-8
        choice -= 1
        self.buttons[choice % len(self.buttons)].invoke()

    def onClick(self, choice: int):
        if (choice == self.correct_person):
            print("Correct")
            self.changePerson()
            return
        else:
            self.buttons[choice]["state"] = tk.DISABLED
            print("Wrong")

root = tk.Tk()
myapp = Game(root)
myapp.mainloop()
