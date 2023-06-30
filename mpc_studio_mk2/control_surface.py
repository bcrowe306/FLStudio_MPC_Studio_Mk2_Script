from framework.control_surface import ControlSurface
from .components.transport import TransportComponent
from .components.channel_navigation import ChannelNavigationComponent
from .components.browser_navigation import BrowserNavigationComponent
from .components.notes_component import NotesComponent
from .components.step_sequencer import StepSequencer
from framework.modes import ModesComponent, Mode
from .controls import Controls

class MPCStudioMk2(ControlSurface):
    def __init__(self) -> None:
        super(MPCStudioMk2, self).__init__(has_meters=True)
        self.transport = TransportComponent()
        self.create_navigation_modes()
        self.create_pad_modes()

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
