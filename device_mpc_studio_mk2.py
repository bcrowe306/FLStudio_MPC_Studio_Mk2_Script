# name=MPC Studio Mk2

import device, transport
from framework.component import Component
from util.state import HandleMidiMsg, HandleUIState
from midi_const import MIDI_STATUS
from surface_def import MPCSurfaceDef
from framework.control import ButtonControl
from color import Skin



class Transport(Component):
    def __init__(self):
        super(Transport, self).__init__()
        self.add_listener('transport.isPlaying', self._on_transport_isPlaying)
        self.test_button = ButtonControl('test_button',MPCSurfaceDef.BUTTON_CHANNEL, MPCSurfaceDef.PLAY,True, skin=Skin.OneColorButton)
        self.add_control(self.test_button)
        self.test_button.subscribe('value', self._on_test_button_value)

    def _on_test_button_value(self, midi_event):
        print(midi_event.status)
    
    def _on_transport_isPlaying(self, isPlaying):
            self.test_button.set_light('FULL') if isPlaying else self.test_button.set_light('DIM')

    # def _on_test_button(self, event):
    #     if event.data2 == 127:
    #         if transport.isPlaying():
    #             transport.stop()
    #         else:
    #             transport.start()
t = Transport()

def OnInit():
    t.activate()

def OnMidiMsg(event):
    HandleMidiMsg(event)

def OnIdle():
    HandleUIState()

def OnDeInit():
    t.deactivate()