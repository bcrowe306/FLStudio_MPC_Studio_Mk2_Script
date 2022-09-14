import device
from midi_const import MIDI_STATUS as mi
from surface_def import MPCSurfaceDef as MPC

def send_sysex_color(pad_number: int, red: int, green: int, blue: int):
    device.midiOutSysex(bytes([0xF0, 0x47, 0x47, 0x04A, 0x65, 0x00, 0x04, pad_number, red, green, blue, 0xF7]))

class MPCButtonColor(object):
    def __init__(self, value):
        self.value = value

    def draw(self, control):
        current_color = getattr(control, 'current_color', None)
        if self.value != current_color or current_color == None:
            device.midiOutMsg(mi.CC_STATUS, control.channel, control.identifier, self.value)
            setattr(control, 'current_color', self.value)



class RGBColor():
    def __init__(self, value: tuple):
        self.value = value

    def draw(self, control):
        red = self.value[0]
        green = self.value[1]
        blue = self.value[2]
        current_color = getattr(control, 'current_color', None)
        if self.value != current_color or current_color == None:
            send_sysex_color(control.pad_number, red, green, blue)
            setattr(control, 'current_color', self.value)
        


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

class PadColor:
    Red = RGBColor(value=(127,0,0))
    Green = RGBColor(value=(0,127,0))
    Blue = RGBColor(value=(0,0,127))
    Yellow = RGBColor(value=(64,64,0))
    Purple = RGBColor(value=(64,0,64))
    Teal = RGBColor(value=(0,64,64))
    Black = RGBColor(value=(0,0,2))
    White = RGBColor(value=(42,42,42))
    Off = RGBColor(value=(0,0,0))
    Default = RGBColor(value=(0,0,2))

class Skin:
    OneColorButton = OneColorButton
    TwoColorButton = TwoColorButton
    Pad = PadColor