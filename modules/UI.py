import tkinter as tk
from tkinter import ttk
import math
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

title = "Formant Synth"


class UI:
    def __init__(self, stream):
        self.stream = stream
        self.root = tk.Tk()
        self.frequency = tk.DoubleVar(value=stream.frequency)

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
            length=500,
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

        # Matplotlibを埋め込み
        fig = Fig(root, self.stream)
        fig.widget.pack()

        # レイアウト
        self.label.pack()
        slider.pack()
        button_play.pack()
        button_stop.pack()

    def _updateFig(self, data):
        plt.cla()  # 現在描写されているグラフを消去
        plt.xlim(0, 500)
        plt.ylim(-1.0, 1.0)
        plt.plot(self.stream.last_data)  # グラフを生成

    def _change_frequency(self, val):
        frequency = self.frequency.get()
        self.label["text"] = math.floor(frequency)
        self.stream.frequency = frequency
        # print("val:%4d" % frequency)

    def _on_destroy(self):
        self.stream.destroy()
        self.root.quit()
        self.root.destroy()


class Fig:
    def __init__(self, tkroot, stream):
        self.stream = stream

        fig = plt.figure()
        anime = animation.FuncAnimation(fig, self._redraw, interval=100)
        canvas = FigureCanvasTkAgg(fig, tkroot)
        canvas.draw()
        self.widget = canvas.get_tk_widget()

    def _redraw(self, data):
        plt.cla()  # 現在描写されているグラフを消去
        plt.xlim(0, 500)
        plt.ylim(-1.0, 1.0)
        plt.plot(self.stream.last_data)  # グラフを生成
