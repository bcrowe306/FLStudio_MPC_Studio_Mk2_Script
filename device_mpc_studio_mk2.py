# name=MPC Studio Mk2

# from framework.component import Component
# from framework.modes import Mode, ModesComponent
from mpc_studio_mk2.control_surface import MPCStudioMk2


mpc_studio_mk2 = MPCStudioMk2()

def OnInit():
    mpc_studio_mk2.OnInit()

def OnMidiMsg(event):
    mpc_studio_mk2.OnMidiMsg(event)
    
def OnRefresh(event):
    mpc_studio_mk2.OnRefresh(event)

def OnIdle():
    mpc_studio_mk2.OnIdle()

def OnUpdateMeters():
    mpc_studio_mk2.OnUpdateMeters()
    
def OnDeInit():
    mpc_studio_mk2.OnDeInit()

def OnUpdateBeatIndicator(event):
    mpc_studio_mk2.OnUpdateBeatIndicator(event)


