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

        self._build()
        self.root.protocol("WM_DELETE_WINDOW", self._on_destroy)  # windowを閉じるとき

    def show(self):
        self.root.mainloop()  # windowを表示

    def _build(self):
        root = self.root
        root.title(title)

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

        UI_Frequency(root, self.stream)
        UI_Amplitude(root, self.stream)

        # レイアウト
        button_play.pack()
        button_stop.pack()

    def _on_destroy(self):
        self.stream.destroy()
        self.root.quit()
        self.root.destroy()


class UI_Frequency:
    def __init__(self, root, stream):
        self.stream = stream
        self.frequency = tk.DoubleVar(value=stream.frequency)

        frame = self._add_frame(root)
        self._add_items(frame)

    def _add_frame(self, root):
        frame = ttk.Frame(root, padding=10)
        frame.pack()
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        return frame

    def _add_items(self, frame):
        col = 0

        # label
        label = ttk.Label(frame, text="Frequency")
        label.grid(row=0, column=col)
        col += 1

        # slider
        slider = ttk.Scale(
            frame,
            from_=100.0,
            to=1000.0,
            length=400,
            variable=self.frequency,
            orient="horizontal",
            command=self._change_frequency,
        )
        slider.grid(row=0, column=col)
        col += 1

        # display value
        self.disp = ttk.Label(frame, text=self.frequency.get())
        self.disp.grid(row=0, column=col)
        col += 1

    def _change_frequency(self, val):
        frequency = self.frequency.get()
        self.disp["text"] = math.floor(frequency)
        self.stream.frequency = frequency
        # print("val:%4d" % frequency)


class UI_Amplitude:
    def __init__(self, root, stream):
        self.stream = stream
        self.amplitude = tk.DoubleVar(value=stream.amplitude)

        frame = self._add_frame(root)
        self._add_items(frame)

    def _add_frame(self, root):
        frame = ttk.Frame(root, padding=10)
        frame.pack()
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        return frame

    def _add_items(self, frame):
        col = 0

        # label
        label = ttk.Label(frame, text="Amplitude")
        label.grid(row=0, column=col)
        col += 1

        # slider
        slider = ttk.Scale(
            frame,
            from_=0.0,
            to=100.0,
            length=400,
            variable=self.amplitude,
            orient="horizontal",
            command=self._change,
        )
        slider.grid(row=0, column=col)
        col += 1

        # display value
        self.disp = ttk.Label(frame, text=self.amplitude.get())
        self.disp.grid(row=0, column=col)
        col += 1

    def _change(self, val):
        amplitude = self.amplitude.get()
        self.disp["text"] = math.floor(amplitude)
        self.stream.amplitude = amplitude


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
