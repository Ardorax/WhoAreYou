#!/usr/bin/python3

import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import random
import os
from enum import Enum

class Modes(Enum):
    Entry=0
    Choice3=1
    Choice9=2


class Game(tk.Frame):
    def __init__(self, master, mode: Modes):
        super().__init__(master)

        self.master.title("Who are you")
        self.mode = mode
        self.picsPath = "pics"
        self.peoples = self.listPeople(self.picsPath)
        self.createWidgets()

    @staticmethod
    def listPeople(path: str):
        # List all student
        peoples = os.listdir(path)
        try:
            peoples.remove(".gitkeep")
        except:
            pass
        return peoples

    @staticmethod
    def getPersonName(path: str):
        return ".".join(path.split(".")[:-1])

    def createButtons(self, row: int, column: int):
        self.textVariables = []
        self.buttons = []
        for y in range(row):
            for x in range(column):
                self.textVariables.append(tk.StringVar())
                button = ttk.Button(self.master, width=30)
                button["textvariable"] = self.textVariables[y * column + x]
                button.grid(row=y + 1, column=x, padx=10, pady=10)
                # Is there a better way to do this?
                button["command"] = lambda y=y, x=x: self.onClick(y * column + x)
                self.buttons.append(button)

    def createEntry(self):
        self.entry = dict()
        self.entry_var = tk.StringVar()
        self.entry_var.trace_add("write", lambda name, index, mode, sv=self.entry_var: self.entry_autocompletion(sv))
        self.entry_tk = tk.Entry(self.master, width=30, textvariable=self.entry_var)
        self.entry_tk.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
        self.entry_tk.bind("<Return>", self.verifyEntry)

        # Skip button
        self.infoLabelVar = tk.StringVar()
        infoLabel = ttk.Label(self.master, textvariable=self.infoLabelVar, justify=tk.CENTER, width=30)
        infoLabel.grid(row=2, column=0, columnspan=3, padx=10, pady=10)
        button = ttk.Button(self.master, width=30, text="Skip")
        button.grid(row=3, column=0, columnspan=3, padx=10, pady=10)
        button["command"] = self.skip
        button.bind("<Return>", self.skip)

    def verifyEntry(self, event=None):
        if (self.entry_var.get() == self.getPersonName(self.correct_person)):
            self.infoLabelVar.set(f"{self.entry_var.get()}\nCorrect!")
            self.correct_person = random.choice(self.peoples)
            self.changePerson()
        else:
            self.infoLabelVar.set(f"No. It's not\n{self.entry_var.get()}")
        self.entry_var.set("")

    def entry_autocompletion(self, event):
        currentText = event.get()
        if len(currentText) < 3:
            return
        # Create a list of all valid names
        props = []
        for name in self.peoples:
            if name.startswith(currentText):
                props.append(name)

        # Auto complete if only one valid name
        if (len(props) == 1):
            self.entry_var.set(self.getPersonName(props[0]))
            self.verifyEntry()

    def createWidgets(self):
        # create a label at center of window with image
        self.imageLabel = ttk.Label(self.master)
        self.imageLabel.grid(row=0, column=0, columnspan=3)
        self.currentImage = None

        match self.mode:
            case Modes.Entry:
                self.createEntry()
                self.changePerson()
            case Modes.Choice3:
                self.createButtons(1,3)
                self.changePerson()
                self.master.bind("<Key>", self.on_keyboard_event)
            case Modes.Choice9:
                self.createButtons(3,3)
                self.changePerson()
                self.master.bind("<Key>", self.on_keyboard_event)

    def skip(self, event=None):
        self.infoLabelVar.set(f"It was\n{self.getPersonName(self.correct_person)}")
        self.changePerson()

    def changePerson(self):
        if self.mode == Modes.Entry:
            self.correct_person = random.choice(self.peoples)
        else:
            self.namesProposals = random.sample(self.peoples, len(self.textVariables))
            self.correct_person = random.choice(self.namesProposals)

            # Texts and enable buttons
            if self.mode != Modes.Entry:
                for i, textVar in enumerate(self.textVariables):
                    textVar.set(self.namesProposals[i])
                    self.buttons[i]["state"] = tk.NORMAL
        self.refreshImage()

    def refreshImage(self):
        if (self.currentImage is not None):
            self.currentImage.close()
        self.currentImage = Image.open(os.path.join(self.picsPath, self.correct_person))
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
        if self.namesProposals[choice] == self.correct_person:
            print("Correct")
            self.changePerson()
            return
        else:
            self.buttons[choice]["state"] = tk.DISABLED
            print("Wrong")

tkApp = tk.Tk()
mode = Modes.Entry
myapp = Game(tkApp, mode)
myapp.mainloop()
