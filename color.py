import device
from midi_const import MIDI_STATUS

class MPCButtonColor(object):
    def __init__(self, value):
        self.value = value

    def draw(self, control):
        device.midiOutMsg(MIDI_STATUS.CC_STATUS, control.channel, control.identifier, self.value)

class OneColorButton:
    Default = MPCButtonColor(1)
    Off = MPCButtonColor(0)
    DIM = MPCButtonColor(1)
    FULL = MPCButtonColor(2)
class TwoColorButton:
    Default = MPCButtonColor(1)
    Off = MPCButtonColor(0)
    DIM_1 = MPCButtonColor(1)
    DIM_2 = MPCButtonColor(2)
    FULL_1 = MPCButtonColor(3)
    FULL_2 = MPCButtonColor(4)

class Skin:
    OneColorButton = OneColorButton
    TwoColorButton = TwoColorButton