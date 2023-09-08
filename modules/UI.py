import tkinter as tk
from tkinter import ttk
import math

title = "Formant Synth"


class UI:
    def __init__(self, stream, frequency):
        self.stream = stream
        self.root = tk.Tk()
        self.frequency = tk.DoubleVar(value=frequency)

        self._buildUI()
        self.root.protocol("WM_DELETE_WINDOW", self._on_destroy)  # windowを閉じるとき

    def show(self):
        self.root.mainloop()  # windowを表示

    def _buildUI(self):
        root = self.root
        root.title(title)

        self.label = ttk.Label(root, text="")
        slider = ttk.Scale(
            root,
            from_=100.0,
            to=1000.0,
            variable=self.frequency,
            orient="horizontal",
            command=self._change_frequency,
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

    def _change_frequency(self, val):
        frequency = self.frequency.get()
        self.label["text"] = math.floor(frequency)
        self.stream.frequency = frequency

        # print("val:%4d" % frequency)

    def _on_destroy(self):
        self.stream.destroy()
        self.root.destroy()
