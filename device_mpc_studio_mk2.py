# name=MPC Studio Mk2

from util.fl_class import FL
from framework.component import Component
from framework.modes import Mode, ModesComponent
from util.state import HandleMidiMsg, HandleUIState
from midi_const import MIDI_STATUS
from surface_def import MPCSurfaceDef
from framework.control import ButtonControl
from color import Skin
import screen
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
mode1 = Mode('mode1', components=[t])
mode2 = Mode('mode2', components=[])
test_modes = ModesComponent('test_modes', default_mode='mode1')
test_modes.add_control('mode1', ButtonControl('mode_button', 0,
                                              MPCSurfaceDef.MODE, skin=Skin.OneColorButton), 'toggled')
test_modes.add_control('mode2', ButtonControl('main_button', 0,
                                              MPCSurfaceDef.MAIN, skin=Skin.OneColorButton), 'toggled')
test_modes.add_mode(mode1)
test_modes.add_mode(mode2)
def OnInit():
    test_modes.activate()

def OnMidiMsg(event):
    HandleMidiMsg(event)

def OnIdle():
    HandleUIState()

def OnDeInit():
    t.deactivate()