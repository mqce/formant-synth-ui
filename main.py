from modules.UI import UI
from modules.AudioStream import AudioStream


frequency = 600.0
stream = AudioStream(frequency)

ui = UI(stream)
ui.show()

# Matplotlibの設定

# fig, ax = plt.subplots()
# x = np.linspace(0, 0.1, int(stream.samplerate * 0.1), endpoint=False)  # 0.1秒分の時間軸
# (line,) = ax.plot(x, stream.last_data)

# def update(frame):
#     line.set_ydata(stream.last_data)
#     return (line,)

# ani = animation.FuncAnimation(fig, update, frames=None, interval=50, blit=True)

# plt.show()
