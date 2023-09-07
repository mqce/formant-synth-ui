import tkinter as tk
from tkinter import ttk
import math


class UI:
    def __init__(self, stream, frequency):
        self.stream = stream
        self.root = tk.Tk()
        self.frequency = tk.DoubleVar(value=frequency)
        self.root.protocol("WM_DELETE_WINDOW", self.on_destroy)

        self.buildUI()

    def buildUI(self):
        root = self.root
        root.title("Sine Wave Generator")

        self.label = ttk.Label(root, text="")
        slider = ttk.Scale(
            root,
            from_=100.0,
            to=1000.0,
            variable=self.frequency,
            orient="horizontal",
            command=self.show_frequency,
        )
        button_play = ttk.Button(
            root,
            text="PLAY",
            command=self.stream.start,
        )
        button_stop = ttk.Button(
            root,
            text="STOP",
            command=self.stream.stop,
        )

        # レイアウト
        self.label.pack()
        slider.pack()
        button_play.pack()
        button_stop.pack()

    def show_frequency(self, val):
        self.label["text"] = math.floor(self.frequency.get())
        print("val:%4d" % self.frequency.get())

    def on_destroy(self):
        self.stream.destroy()
        self.root.destroy()

    def show(self):
        # windowを表示
        self.root.mainloop()
