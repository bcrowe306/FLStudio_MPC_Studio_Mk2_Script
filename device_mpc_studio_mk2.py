# name=MPC Studio Mk2
import channels, device, mixer
import time
from mpc_studio_mk2.control_surface import MPCStudioMk2

MPC = MPCStudioMk2()

def OnInit():
    MPC.OnInit()
    
def OnMidiMsg(event):
    MPC.OnMidiMsg(event)

def OnIdle():
    MPC.OnIdle()

def OnDeInit():
    MPC.OnDeInit()

def OnRefresh(event):
    MPC.OnRefresh(event)

def OnUpdateBeatIndicator(event):
    device.midiOutMsg(176, 0, 9, event) 
    MPC.OnUpdateBeatIndicator(event)

# t = Transport()
# mode1 = Mode('mode1', components=[t])
# mode2 = Mode('mode2', components=[])
# test_modes = ModesComponent('test_modes', default_mode='mode1')
# test_modes.add_control('mode1', ButtonControl('mode_button', 0,
#                                               MPCSurfaceDef.MODE, skin=Skin.OneColorButton), 'toggled')
# test_modes.add_control('mode2', ButtonControl('main_button', 0,
#                                               MPCSurfaceDef.MAIN, skin=Skin.OneColorButton), 'toggled')
# test_modes.add_mode(mode1)
# test_modes.add_mode(mode2)