from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget

from GUI.PulsePalGUI import PulsePalChannelWidget
from src.PulsePal import PulsePalObject
from src.PulsePalHelpers import PulsePalOutputChannel, DummyPulsePalObject


class testWin(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('GUI/channelwidget.ui', self)
        self.show()


app = QApplication([])

p = DummyPulsePalObject(None)
c = PulsePalOutputChannel(channel_id=1, pulsepal=p)
t = PulsePalChannelWidget(channel=c)
t.show()

# Start the event loop.
app.exec()


# Your application won't reach here until you exit and the event
# loop has stopped.


