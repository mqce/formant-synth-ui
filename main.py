import math
import numpy as np
import sounddevice as sd
import tkinter as tk
from tkinter import ttk

#
# class App:
#     def __init__(self, root):
#         self.frequency = tk.DoubleVar(value=440.0)  # 初期周波数を440Hzに設定

#         self.slider = ttk.Scale(
#             root, from_=100.0, to=1000.0, variable=self.frequency,
#             orient="horizontal", label="Frequency (Hz)"
#         )
#         self.slider.pack(pady=20)

#         self.button = ttk.Button(root, text="Play sound", command=self.play_sound)
#         self.button.pack(pady=20)

#     def play_sound(self):
#         fs = 44100  # サンプリング周波数
#         t = np.linspace(0, 1, int(fs), endpoint=False)  # 1秒間の時間軸
#         x = 0.5 * np.sin(2 * np.pi * self.frequency.get() * t)  # サイン波の生成
#         sd.play(x, samplerate=fs)  # サイン波の再生


def play_sine_wave(frequency=440.0, duration=1.0, amplitude=0.5, samplerate=44100):
    """
    指定された周波数、持続時間、振幅、サンプリングレートでサイン波を再生します。

    :param frequency: サイン波の周波数 (デフォルト: 440.0Hz)
    :param duration: サイン波の持続時間 (デフォルト: 1.0秒)
    :param amplitude: サイン波の振幅 (デフォルト: 0.5)
    :param samplerate: サンプリングレート (デフォルト: 44100Hz)
    """
    t = np.arange(int(samplerate * duration)) / samplerate  # 時間軸
    print(t)
    x = amplitude * np.sin(2 * np.pi * frequency * t)  # サイン波の生成
    sd.play(x, samplerate=samplerate)


class ContinuousSineWave:
    def __init__(self, frequency=440.0, amplitude=0.5, samplerate=44100):
        self.frequency = frequency
        self.amplitude = amplitude
        self.samplerate = samplerate

        # ストリームを開始
        self.stream = sd.OutputStream(
            samplerate=self.samplerate, channels=1, callback=self.callback
        )

    def callback(self, outdata, frames, time, status):
        t = (
            np.arange(frames) + time.outputBufferDacTime * self.samplerate
        ) / self.samplerate
        outdata[:, 0] = self.amplitude * np.sin(2 * np.pi * self.frequency * t)

    def start(self):
        self.stream.start()

    def stop(self):
        self.stream.stop()

    def destroy(self):
        self.stream.close()


stream = ContinuousSineWave(frequency=440.0)

root = tk.Tk()
root.title("Sine Wave Generator")

frequency = tk.DoubleVar(value=440.0)

label = ttk.Label(root, text=frequency.get())


def show_frequency(self):
    label["text"] = math.floor(frequency.get())
    print("val:%4d" % frequency.get())


slider = ttk.Scale(
    root,
    from_=100.0,
    to=1000.0,
    variable=frequency,
    orient="horizontal",
    command=show_frequency,
)
button_play = ttk.Button(
    root,
    text="PLAY",
    command=stream.start,
)
button_stop = ttk.Button(
    root,
    text="STOP",
    command=stream.stop,
)

root.protocol("WM_DELETE_WINDOW", stream.destroy)

# レイアウト
label.pack()
slider.pack()
button_play.pack()
button_stop.pack()
# app = App(root)

# windowを表示
root.mainloop()

# tk._test()
