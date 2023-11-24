import tkinter as tk
from tkinter import ttk

from src.GameBase import GameBase


class GameEntry(GameBase):
    def __init__(self, master, picsPath):
        super().__init__(master, picsPath)

    def createWidgets(self):
        super().createWidgets()

        self.entry_var = tk.StringVar()
        self.entry_var.trace_add("write", lambda name, index, mode, sv=self.entry_var: self.entry_autocompletion(sv))
        self.entry_tk = tk.Entry(self.master, width=30, textvariable=self.entry_var)
        self.entry_tk.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
        self.entry_tk.bind("<Return>", self.verifyEntry)
    
        self.lastLabel = ttk.Label(self.master, text="")
        self.lastLabel.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        skip_button = ttk.Button(self.master, width=30, text="Skip", command=self.skip)
        skip_button.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

    def entry_autocompletion(self, sv):
        currentText = sv.get()
        if len(currentText) < 3:
            return
        currentText = self.getPersonName(currentText)
        props = [name for name in self.peoples if self.getPersonName(name).startswith(currentText)]
        if len(props) == 1:
            self.entry_var.set(self.getPersonName(props[0]))
            self.verifyEntry()
    
    def setLabel(self, text, color):
        labelText = tk.StringVar()
        labelText.set(text)
        if self.lastLabel is not None:
            self.lastLabel.destroy()
        label = ttk.Label(self.master, textvariable=labelText, foreground=color)
        label.grid(row=2, column=0, columnspan=3, padx=10, pady=10)
        self.master.after(2000, lambda: labelText.set(""))
        self.lastLabel = label

    def correct(self, guess):
        self.setLabel(f"{self.getPersonName(guess)} is correct!", "green")
        self.entry_var.set("")
        self.changePerson()
    
    def wrong(self, guess):
        self.setLabel(f"{self.getPersonName(guess)} is wrong!", "red")
        self.entry_var.set("")

    def verifyEntry(self, event=None):
        self.guess(
            guess=self.entry_var.get(),
            onCorrect=lambda: self.correct(self.entry_var.get()),
            onWrong=lambda: self.wrong(self.entry_var.get())
        )

    def skip(self):
        self.resetStreaks()
        self.entry_var.set("")
        self.setLabel(f"It was {self.getPersonName(self.correct_person)}", "blue")
        self.changePerson()
