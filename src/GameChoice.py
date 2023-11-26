import random
import tkinter as tk
from tkinter import ttk
from src.GameBase import GameBase


class GameChoice(GameBase):
    def __init__(self, master, picsPath, num_choices):
        self.num_choices = num_choices
        super().__init__(master, picsPath)

    def createWidgets(self):
        super().createWidgets()
        rows, columns = self.determineLayout()
        self.createButtons(rows, columns)

    def determineLayout(self):
        if self.num_choices == 3:
            return 1, 3
        elif self.num_choices == 9:
            return 3, 3
        else:
            raise ValueError("Invalid number of choices")

    def createButtons(self, row, column):
        self.buttons = []
        for y in range(row):
            for x in range(column):
                button = ttk.Button(
                    self.master,
                    width=30,
                    command=lambda y=y, x=x: self.onClick(y * column + x),
                )
                button.grid(row=y + 1, column=x, padx=10, pady=10)
                self.buttons.append(button)
        self.changePerson()

    def changePerson(self):
        super().changePerson()
        self.namesProposals = random.sample(
            list(filter(lambda x: x != self.correct_person, self.peoples)),
            self.num_choices - 1,
        ) + [self.correct_person]

        random.shuffle(self.namesProposals)
        for i, button in enumerate(self.buttons):
            button["text"] = self.getPersonName(self.namesProposals[i])
            button["state"] = tk.NORMAL

    def onWrong(self, choice):
        self.buttons[choice]["state"] = tk.DISABLED

    def onClick(self, choice):
        self.guess(
            guess=self.getPersonName(self.namesProposals[choice]),
            onCorrect=lambda: self.changePerson(),
            onWrong=lambda: self.onWrong(choice),
        )
