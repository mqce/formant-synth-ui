from modules.UI import UI
from modules.AudioStream import AudioStream


frequency = 550.0
stream = AudioStream(frequency)

ui = UI(stream)
ui.show()
