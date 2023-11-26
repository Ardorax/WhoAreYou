#!/usr/bin/python3

import tkinter as tk
from enum import Enum
from src.GameChoice import GameChoice
import sys

from src.GameEntry import GameEntry


class Modes(Enum):
    Entry = 0
    Choice3 = 1
    Choice9 = 2


tkApp = tk.Tk()
tkApp.title("Who Are You")

if len(sys.argv) > 1:
    selected_mode = sys.argv[1].lower()
else:
    selected_mode = "entry"

mode = None

if selected_mode == "entry":
    mode = Modes.Entry
elif selected_mode == "choice3":
    mode = Modes.Choice3
elif selected_mode == "choice9":
    mode = Modes.Choice9

if mode == Modes.Entry:
    myapp = GameEntry(tkApp, "pics")
elif mode == Modes.Choice3:
    myapp = GameChoice(tkApp, "pics", 3)
elif mode == Modes.Choice9:
    myapp = GameChoice(tkApp, "pics", 9)
else:
    raise ValueError("Invalid mode selected")

myapp.mainloop()
