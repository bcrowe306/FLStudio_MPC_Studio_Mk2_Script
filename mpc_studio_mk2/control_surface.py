from framework.control_surface import ControlSurface
from .components.transport import TransportComponent
from .components.channel_navigation import ChannelNavigationComponent
from .components.browser_navigation import BrowserNavigationComponent
from .components.notes_component import NotesComponent
from .components.step_sequencer import StepSequencer
from framework.modes import ModesComponent, Mode
from .surface_def import MPCSurfaceDef as MPC
from framework.util.midi import MIDI_STATUS
from .controls import Controls
import device, screen

TextScrollPause = 10
TextScrollSpeed = 2
TextDisplayTime = 4000

TimedTextRow = 1
FPSRow = 3
FireFontSize = 16
TextOffset = -4
TextRowHeight = 20

Idle_Interval = 100
Idle_Interval_Max = 8

# seconds to keep screen active (screen has its own timeout which will kick in after this)
ScreenActiveTimeout = 30
ScreenAutoTimeout = 10

class MPCStudioMk2(ControlSurface):
    def __init__(self) -> None:
        super(MPCStudioMk2, self).__init__(meters=True)
        self.transport = TransportComponent()
        self.create_navigation_modes()
        self.create_pad_modes()

    def OnInit(self):
        device.setHasMeters() if self.meters else None
        return super().OnInit()
    
    def create_pad_modes(self):
        self.pad_modes = ModesComponent(
            name='pad_modes',
            default_mode='step_sequencer'
        )
        self.pad_modes.add_mode(
            Mode(name='notes', components=[
                 NotesComponent()], active_color='FULL_2', inactive_color='DIM_1')
        )
        self.pad_modes.add_mode(
            Mode(name='step_sequencer', components=[
                 StepSequencer(name='step_sequencer')], active_color='FULL_2', inactive_color='DIM_1')
        )
        self.pad_modes.add_control(
            'step_sequencer', control=Controls.pad_bank_ae, event_name='toggled')
        self.pad_modes.add_control(
            'notes', control=Controls.pad_bank_bf, event_name='toggled')
        
    def create_navigation_modes(self):
        self.navigation_modes = ModesComponent(
            name='navigation_modes',
            default_mode='channel'
        )
        self.navigation_modes.add_mode(
            Mode(name='browser', components=[
                 BrowserNavigationComponent()], active_color='FULL_1', inactive_color='DIM_1')
        )
        self.navigation_modes.add_mode(
            Mode(name='channel', components=[
                 ChannelNavigationComponent()], active_color='FULL_1', inactive_color='DIM_1')
        )
        self.navigation_modes.add_control(
            'browser', control=Controls.browse_button, event_name='toggled')
        self.navigation_modes.add_control(
            'channel', control=Controls.track_select_button, event_name='toggled')
