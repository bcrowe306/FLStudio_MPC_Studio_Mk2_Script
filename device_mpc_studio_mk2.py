# name=MPC Studio Mk2

import device, transport
from util.fl_class import FL
from framework.component import Component
from util.state import HandleMidiMsg, HandleUIState
from midi_const import MIDI_STATUS
from surface_def import MPCSurfaceDef
from framework.control import ButtonControl
from color import Skin

fl = FL()


class Transport(Component):
    def __init__(self):
        super(Transport, self).__init__()
        self.test_button = ButtonControl('test_button',MPCSurfaceDef.BUTTON_CHANNEL, MPCSurfaceDef.PLAY,True, skin=Skin.OneColorButton)

    @Component.subscribe('test_button', 'toggled')
    def _on_test_button_toggled(self, toggled):
        fl.transport.start() if toggled else fl.transport.stop()
    
    @Component.listens('transport.isPlaying')
    def _on_transport_isPlaying(self, isPlaying):
            self.test_button.set_light('FULL') if isPlaying else self.test_button.set_light('DIM')

t = Transport()

def OnInit():
    t.activate()

def OnMidiMsg(event):
    HandleMidiMsg(event)

def OnIdle():
    HandleUIState()

def OnDeInit():
    t.deactivate()