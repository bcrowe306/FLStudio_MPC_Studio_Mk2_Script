import device
from framework.util.midi import MIDI_STATUS
from .util import mpc_pad_sysex

class MPCButtonColor(object):
    def __init__(self, value):
        self.value = value

    def draw(self, control):
        device.midiOutMsg(MIDI_STATUS.CC_STATUS, control.channel, control.identifier, self.value)

def mpc_pad_draw(self, control, red, green, blue):
    sysex = mpc_pad_sysex(control.number, red, green, blue)
    device.midiOutSysex(bytes(sysex))

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
    mpc_pad_draw = mpc_pad_draw
