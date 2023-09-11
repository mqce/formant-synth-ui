import numpy as np
import sounddevice as sd
from scipy import signal


class AudioStream:
    def __init__(self, frequency=440.0, amplitude=5, samplerate=44100):
        self.frequency = frequency
        self.amplitude = amplitude
        self.samplerate = samplerate
        self.phase = 0  # 追加: 継続的に更新されるフェーズ変数

        # 最後に生成された音声データを保持するためのバッファ
        self.last_data = np.zeros(int(self.samplerate * 0.1))  # 0.1秒分

        # ストリームを開始
        self.stream = sd.OutputStream(
            samplerate=self.samplerate, channels=1, callback=self.callback
        )

    def callback(self, outdata, frames, time, status):
        t = np.arange(frames) / self.samplerate

        # 声帯の振動
        sig = self.amplitude * np.sin(2 * np.pi * self.frequency * t + self.phase)
        formants = [
            (700 - 65, 700 + 65),
            (1220 - 35, 1220 + 35),
            (2600 - 80, 2600 + 80),
        ]  # あ
        outdata[:, 0] = self.formant_synthesis(sig, formants)

        # f0 = self.frequency
        # outdata[:, 0] = (
        #     0.07 * np.sin(2 * np.pi * t * f0 * 1 + self.phase)
        #     + 0.09 * np.sin(2 * np.pi * t * f0 * 2 + self.phase)
        #     + 0.08 * np.sin(2 * np.pi * t * f0 * 3 + self.phase)
        #     + 0.19 * np.sin(2 * np.pi * t * f0 * 4 + self.phase)
        #     + 0.08 * np.sin(2 * np.pi * t * f0 * 5 + self.phase)
        #     + 0.07 * np.sin(2 * np.pi * t * f0 * 6 + self.phase)
        # )

        # プツプツというノイズは、サイン波の連続性が失われている場合や、バッファとの境界でのフェーズの不連続性に起因する可能性があります。
        # この問題を解消するためには、フェーズの連続性を保つための変数を導入して、コールバックが呼ばれるたびにフェーズを継続的に更新することが必要です。

        # 最後のフェーズを更新して次回のコールバックに渡す
        self.phase += 2 * np.pi * self.frequency * frames / self.samplerate
        self.phase %= 2 * np.pi  # 0から2πの範囲に保つ

        # 最後に生成された音声データを保存
        self.last_data = np.copy(outdata[:, 0])

    # 帯域通過フィルタの設計
    # https://atatat.hatenablog.com/entry/data_proc_python5
    def bandpass_filter(self, x, freq_low, freq_high):
        gpass = 3  # 通過域端最大損失[dB]
        gstop = 40  # 阻止域端最小損失[dB]
        nyquist = 0.5 * self.samplerate  # ナイキスト周波数
        wp = freq_low / nyquist  # ナイキスト周波数で正規化
        ws = freq_high / nyquist
        # N, Wn = signal.buttord(wp, ws, gpass, gstop)  # N:フィルタ次数 Wn:カットオフ周波数
        N = 4
        b, a = signal.butter(N, [wp, ws], "band")  # フィルタ伝達関数の分子と分母を計算
        y = signal.filtfilt(b, a, x)  # 信号に対してフィルタをかける

        return y

    # Formant synthesis
    def formant_synthesis(self, voice_signal, formants):
        sig = np.zeros_like(voice_signal)
        for freq_low, freq_high in formants:
            sig += self.bandpass_filter(voice_signal, freq_low, freq_high)
        return sig

    def start(self):
        self.stream.start()

    def stop(self):
        self.stream.stop()

    def destroy(self):
        self.stream.close()
