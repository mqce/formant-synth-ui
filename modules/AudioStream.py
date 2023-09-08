import numpy as np
import sounddevice as sd


class AudioStream:
    def __init__(self, frequency=440.0, amplitude=0.5, samplerate=44100):
        self.frequency = frequency
        self.amplitude = amplitude
        self.samplerate = samplerate
        self.phase = 0  # 追加: 継続的に更新されるフェーズ変数

        # ストリームを開始
        self.stream = sd.OutputStream(
            samplerate=self.samplerate, channels=1, callback=self.callback
        )

    def callback(self, outdata, frames, time, status):
        # t = (
        #     np.arange(frames) + time.outputBufferDacTime * self.samplerate
        # ) / self.samplerate
        # outdata[:, 0] = self.amplitude * np.sin(2 * np.pi * self.frequency * t)

        t = np.arange(frames) / self.samplerate
        outdata[:, 0] = self.amplitude * np.sin(
            2 * np.pi * self.frequency * t + self.phase
        )
        # プツプツというノイズは、サイン波の連続性が失われている場合や、バッファとの境界でのフェーズの不連続性に起因する可能性があります。
        # この問題を解消するためには、フェーズの連続性を保つための変数を導入して、コールバックが呼ばれるたびにフェーズを継続的に更新することが必要です。

        # 最後のフェーズを更新して次回のコールバックに渡す
        self.phase += 2 * np.pi * self.frequency * frames / self.samplerate
        self.phase %= 2 * np.pi  # 0から2πの範囲に保つ

    def start(self):
        self.stream.start()

    def stop(self):
        self.stream.stop()

    def destroy(self):
        self.stream.close()
