from modules.UI import UI
from modules.AudioStream import AudioStream


frequency = 600.0
stream = AudioStream(frequency)

ui = UI(stream, frequency)
ui.show()
