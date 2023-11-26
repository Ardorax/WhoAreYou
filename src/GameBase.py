import math
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import random
import os
import json


class GameBase(tk.Frame):
    def __init__(self, master, picsPath):
        super().__init__(master)
        self.master = master
        self.picsPath = picsPath
        self.peoples = self.listPeople(self.picsPath)
        self.streaks = 0
        self.createWidgets()

    @staticmethod
    def listPeople(path: str):
        peoples = os.listdir(path)
        try:
            peoples.remove(".gitkeep")
        except:
            pass
        return peoples

    @staticmethod
    def getPersonName(path: str):
        path = path.replace(".jpg", "")
        path = "".join([i if i.isalpha() else " " for i in path])
        path = path.strip()
        path = " ".join([i.capitalize() for i in path.split()])
        return path

    def createWidgets(self):
        self.imageLabel = ttk.Label(self.master)
        self.imageLabel.grid(row=0, column=0, columnspan=3)
        self.currentImage = None
        self.correct_person = random.choice(self.peoples)
        self.refreshImage()

        self.streaksVar = tk.StringVar()
        self.streaksVar.set("Streaks: 0")
        self.streaksLabel = ttk.Label(self.master, textvariable=self.streaksVar)
        self.streaksLabel.grid(row=4, column=0, columnspan=3, padx=10, pady=10)

    def addStreak(self, amount):
        self.streaks += amount
        self.streaksVar.set(f"Streaks: {self.streaks}")

    def resetStreaks(self):
        self.streaks = 0
        self.streaksVar.set(f"Streaks: {self.streaks}")

    def refreshImage(self):
        if self.currentImage is not None:
            self.currentImage.close()
        self.currentImage = Image.open(os.path.join(self.picsPath, self.correct_person))
        self.imgobj = ImageTk.PhotoImage(self.currentImage)
        self.imageLabel["image"] = self.imgobj

    def changePerson(self):
        peoples = [*self.peoples]
        random.shuffle(peoples)
        data = self.getStatuses()

        order = list(
            sorted(
                peoples,
                key=lambda x: 0
                if x not in data
                else data[x]["correct"] / (data[x]["wrong"] + data[x]["correct"]),
            )
        )

        for i in range(len(order)):
            score = random.randint(0, 10)
            if score == 0:
                self.correct_person = order[i]
                break

        self.refreshImage()

    def getStatuses(self):
        if os.path.exists("data.json"):
            with open("data.json", "r") as f:
                data = json.load(f)
        else:
            data = {}
        return data

    def addStatus(self, toguess, found):
        data = self.getStatuses()
        if toguess not in data:
            data[toguess] = {"correct": 0, "wrong": 0}
        if found:
            data[toguess]["correct"] += 1
        else:
            data[toguess]["wrong"] += 1
        with open("data.json", "w") as f:
            json.dump(data, f)

    def guess(self, guess, onCorrect, onWrong):
        toguess = self.getPersonName(self.correct_person)
        if guess == self.getPersonName(self.correct_person):
            self.addStreak(1)
            self.addStatus(toguess, True)
            onCorrect()
        else:
            self.resetStreaks()
            self.addStatus(toguess, False)
            onWrong()
