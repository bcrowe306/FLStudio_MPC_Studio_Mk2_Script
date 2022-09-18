# name=MPC Studio Mk2
import device
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
    MPC.OnUpdateBeatIndicator(event)


