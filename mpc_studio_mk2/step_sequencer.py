from framework.component import Component
from framework.controls.jog_control import JogControl
from util.fl_class import FL
from framework.control import MPCPadsControl
from surface_def import MPCSurfaceDef
StepColorState = {
    0: (0,0,2),
    1: (5,40,64),
    2: (64,5,64),
    3: (127,10,0)
}

class StepSequencer(Component):
    def __init__(self, pads : MPCPadsControl, auto_active=True, *a, **k):
        super().__init__(auto_active, *a, **k)
        self.jog_wheel = JogControl(name='jog_wheel', channel=0, identifier=100, inc_value=1, dec_value=127)
        self._current_step_index = -1
        self.pads : MPCPadsControl = pads
        self.current_pattern_steps = None
        self.current_pattern_number = None
        self.current_pattern_length = None
        self.shift = 0
        

        self.selected_channel = None

    @Component.subscribe('jog_wheel', 'jogged')
    def _on_jogged(self, value):
        channel_length = FL.channels.channelCount()
        next_index = 0
        if value:
            next_index = self.selected_channel + 1 if self.selected_channel + 1 < channel_length else 0
        else:
            next_index = self.selected_channel -1 if self.selected_channel - 1 >= 0 else channel_length - 1
        FL.channels.selectOneChannel(next_index)
        

    @Component.subscribe('pads', 'step_pressed')
    def _on_step_pressed(self, step, event):
        selected_step_index = step + self.shift
        selected_step_bit = FL.channels.getGridBit(self.selected_channel, selected_step_index)
        FL.channels.setGridBit(self.selected_channel, selected_step_index, 0) if selected_step_bit == 1 else FL.channels.setGridBit(self.selected_channel, selected_step_index, 1)

    @Component.listens('mixer.getSongStepPos')
    def _update_pad_led(self, step):
        self._current_step_index = step
        self.update_pad_steps()

    def initialize(self):
        self.update_pad_steps()
    
    @Component.listens('OnRefresh')
    def update_pad_steps(self, _ = None):
        self.current_pattern_number = FL.patterns.patternNumber()
        self.current_pattern_length = FL.patterns.getPatternLength(self.current_pattern_number)
        self.selected_channel= FL.channels.selectedChannel()
        self.get_pattern_steps()
        colors = self.get_pad_colors(self._current_step_index)
        self.pads.set_lights(colors)

    def get_pattern_steps(self):
        pattern = [] 
        for step_index in range(self.current_pattern_length):
            grid_bit = FL.channels.getGridBit(self.selected_channel, step_index)
            pattern.append(grid_bit)
        self.current_pattern_steps = pattern
    
    def get_pad_colors(self, current_step_index = -1):

        colors = []
        pad_steps_length = len(self.pads._pads)
        self.shift = 0 if current_step_index < pad_steps_length else ( current_step_index // pad_steps_length) * 16
        # Loop over pad number to determine colors for each pad according to the pattern
        for index in range(pad_steps_length):
            shifted_index = index + self.shift
            if shifted_index >= len(self.current_pattern_steps):
                colors.append(StepColorState[0])
                continue
            step = self.current_pattern_steps[shifted_index]
            if shifted_index == current_step_index:
                step = 3 if step == 1 else 2
            colors.append(StepColorState[step])
        return colors

    def activate(self):
        self.pads.activate()
        self.initialize()
        return super().activate()

    def deactivate(self):
        self.pads.deactivate()
        return super().activate()