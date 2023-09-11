import numpy as np
from scipy.signal import lfilter, butter, filtfilt
import sounddevice as sd
import math


def bandpass_filter(data, center_freq, bandwidth, fs, order=4):
    low = (center_freq - bandwidth / 2) / (0.5 * fs)
    high = (center_freq + bandwidth / 2) / (0.5 * fs)
    b, a = butter(order, [low, high], btype="band")
    return filtfilt(b, a, data)


# def bandpass_filter(data, center_freq, Q, fs, order=4):
#     nyquist = 0.5 * fs  # ナイキスト周波数
#     bandwidth = center_freq / Q # Q = width of the formant
#     low = (center_freq - bandwidth/2) / nyquist
#     high = (center_freq + bandwidth/2) / nyquist
#     b, a = butter(order, [low, high], btype='band')
#     return lfilter(b, a, data)


# ソース信号のモデル：Liljencrants-Fant (LF) モデル
def lf_model(Ee, Tp, Te, duration, fs=44100):
    t = np.linspace(0, duration, int(fs * duration), endpoint=False)
    E0 = 0.6
    Ta = Tp * E0 / Ee
    E0_Ta = E0 / Ta

    # 3つのフェーズに基づくLFモデル
    e = np.piecewise(
        t,
        [(t < Ta), (t >= Ta) & (t < Tp), (t >= Tp) & (t < Te)],
        [
            lambda t: E0_Ta * t,
            lambda t: E0 * (1 - np.exp(-Ee * (t - Ta))),
            lambda t: (1 - np.exp(-Ee * (Te - t))) / (1 - np.exp(-Ee * (Te - Tp))),
        ],
    )
    return e


def glottis_output(duration=1.5, fs=44100):
    # LFモデルのパラメータの例
    # Ee: グロッタルパルスの最大振幅。この値は、音声の強度や声の強さに関連しています。実際の音声データから直接測定することができます。
    # Tp: グロッタルパルスのピークが発生するまでの時間。これは、声帯の振動周期の一部として考えることができます。実際の音声データのグロッタルパルスから直接測定することができます。
    # Te: グロッタルパルスの励起が終了する時間。この値は、音声の持続時間や音声の長さに関連しています。実際の音声データから直接測定することができます。
    # Ta: 帰還の開始からグロッタルパルスの終了までの時間。これは、声の品質や特性に影響を与える可能性があります。
    Ee = 0.9
    Tp = 0.004  # 成人男性で5msくらい、子供なら2-3ms
    Te = 0.005  #
    delta = 0.02

    """
    Rd = 2
    if Rd < 0.5:
        Rd = 0.5
    if Rd > 2.7:
        Rd = 2.7
    Ra = -0.01 + 0.048 * Rd
    Rk = 0.224 + 0.118 * Rd
    Rg = (Rk / 4) * (0.5 + 1.2 * Rk) / (0.11 * Rd - Ra * (0.5 + 1.2 * Rk))

    Ta = Ra
    Tp = 1 / (2 * Rg)
    Te = Tp + Tp * Rk

    epsilon = 1 / Ta
    shift = math.exp(-epsilon * (1 - Te))
    Delta = 1 - shift
    # divide by this to scale RHS

    print(Tp, Te, Delta)  # 0.4482675485171186 0.5909959359649691 0.9999994434737794
    """

    glottal_pulse = lf_model(Ee, Tp, Te, delta)

    # ホワイトノイズをのせる
    white_noise = np.random.normal(0, 1, glottal_pulse.shape)

    pulse = 0.9 * glottal_pulse + 0.0 * white_noise

    signal = np.tile(pulse, int(duration / delta))

    # # 疑似的な声帯パルス列の生成
    # T0 = int(fs / 100)  # 基本周波数（約100Hz）に対応するサンプル数
    # glottal_pulse = np.zeros(T0)
    # glottal_pulse[:10] = 1  # 単純な三角波を生成
    # num_pulses = int(duration * fs / T0)
    # signal = np.tile(glottal_pulse, num_pulses)

    return signal


def vowel_synthesis(formants, duration=1.5, fs=44100):
    source_signal = glottis_output(duration, fs)

    signal = np.zeros_like(source_signal)
    for formant in formants:  # f1~f6
        signal += (
            bandpass_filter(source_signal, formant[0], formant[1], fs) * formant[2]
        )

    # 波形の正規化
    signal /= np.max(np.abs(signal))

    return signal


formants_list1 = [
    [
        (800, 80, 0.5),
        (1200, 80, 0.5),
        (2300, 100, 0.5),
        (2800, 140, 0.5),
        (3800, 190, 0.5),
        (4800, 240, 0.5),
    ],  # a
    [(800, 80, 0.5), (1200, 80, 0.6)],  # a
    [(600, 60, 0.6), (2100, 150, 0.8)],  # e
    [(300, 50, 0.5), (2300, 180, 0.5)],  # i
    [(270, 60, 0.5), (2300, 180, 0.09), (3000, 100, 0.18)],  # i
    [(400, 80, 0.6), (750, 60, 0.5)],  # o
    [(350, 50, 0.6), (1800, 100, 0.7)],  # u
]

# 各母音のフォルマントを設定（中心周波数, バンド幅, ゲインのトリプルとして）
formants_list2 = [
    [(700, 80, 0.8), (1200, 80, 0.2)],  # a
    [(600, 60, 0.8), (2100, 150, 0.2)],  # e
    [(270, 60, 0.8), (2300, 170, 0.2)],  # i
    [(400, 80, 0.8), (750, 60, 0.2)],  # o
    [(350, 50, 0.8), (1800, 100, 0.2)],  # u
]


"""
The formant frequencies will be: 
F1 = 800 Hz, F2 = 1200 Hz, F3 = 2300 Hz, F4 = 2800 Hz.
The frequencies of the higher formants will be at intervals of 1000 Hz, starting from F4.
Therefore, F5 = 3800 Hz, F6 = 4800 Hz, F7 = 5800 Hz, and so on. 
You would typically choose this value as 1000 / 1100 Hz for a male / female voice.


The bandwidths will be B1 = 80 Hz, B2 = 80 Hz, B3 = 100 Hz.
The bandwidths of the fourth and higher formants will be 0.05 times their frequency.
Therefore, B4 = 140 Hz, B5 = 190 Hz, B6 = 240 Hz, B7 = 290 Hz, and so on.
"""


def generate_adsr_envelope(
    attack, decay, sustain_level, sustain_duration, release, total_length, fs
):
    # 各フェーズのサンプル数を計算
    attack_samples = int(attack * fs)
    decay_samples = int(decay * fs)
    sustain_samples = int(sustain_duration * fs)
    release_samples = int(release * fs)

    # 各フェーズのエンベロープを生成
    attack_envelope = np.linspace(0, 1, attack_samples)
    decay_envelope = np.linspace(1, sustain_level, decay_samples)
    sustain_envelope = np.ones(sustain_samples) * sustain_level
    release_envelope = np.linspace(sustain_level, 0, release_samples)

    # 全エンベロープを結合
    envelope = np.concatenate(
        [attack_envelope, decay_envelope, sustain_envelope, release_envelope]
    )

    # 全体の長さに合わせてエンベロープを拡張・切り取り
    if len(envelope) < total_length:
        envelope = np.concatenate([envelope, np.zeros(total_length - len(envelope))])
    else:
        envelope = envelope[:total_length]

    return envelope


# エンベロープのパラメータ
attack = 0.01  # 10ms
decay = 0.02  # 20ms
sustain_level = 0.9  # 70%
sustain_duration = 0.5  # 500ms
release = 0.1  # 100ms

fs = 44100
signal_length = 1  # 1秒
envelope = generate_adsr_envelope(
    attack, decay, sustain_level, sustain_duration, release, signal_length * fs, fs
)


# 各母音を生成して連結
waveforms = []
for formants in formants_list2:
    waveform = vowel_synthesis(formants, 1) * envelope
    waveforms.append(waveform)

combined_waveform = np.concatenate(waveforms)

# sounddeviceを使用して音声を再生
sd.play(combined_waveform, samplerate=44100)
sd.wait()  # 再生が終わるのを待つ
