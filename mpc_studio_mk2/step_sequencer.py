from framework.component import Component
from framework.controls.jog_control import JogControl
from .custom_controls.mpc_pads import MPCPadsControl
from framework.util.colors import pad_color
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
        self.track_color = None

    def StepColorState(self, group, step_value):
        r,g,b = self.track_color
        shift = 5
        g = round(g / shift)
        b = round(b / shift)
        group2 = (r,g,b)
        state = {
            0:{
                0: pad_color(self.track_color, 1),
                1: pad_color(self.track_color, 40 ),
                2: pad_color(self.track_color, 120),
                3: (127,127 ,127)
            },
            1: {
                0: pad_color(group2, 1),
                1: pad_color(group2, 40 ),
                2: pad_color(group2, 120),
                3: (127,127,127)
            }
        }
        return state[group][step_value]


    @Component.subscribe('jog_wheel', 'jogged')
    def _on_jogged(self, value):
        channel_length = self.fl.channels.channelCount()
        next_index = 0
        if value:
            next_index = self.selected_channel + 1 if self.selected_channel + 1 < channel_length else 0
        else:
            next_index = self.selected_channel -1 if self.selected_channel - 1 >= 0 else channel_length - 1
        self.fl.channels.selectOneChannel(next_index)

    @Component.subscribe('pads', 'step_pressed')
    def _on_step_pressed(self, step, event):
        selected_step_index = step + self.shift
        selected_step_bit = self.fl.channels.getGridBit(self.selected_channel, selected_step_index)
        self.fl.channels.setGridBit(self.selected_channel, selected_step_index, 0) if selected_step_bit == 1 else self.fl.channels.setGridBit(self.selected_channel, selected_step_index, 1)

    @Component.listens('mixer.getSongStepPos')
    def _update_pad_led(self, step):
        self._current_step_index = step
        self.update_pad_steps()

    def initialize(self):
        self.update_pad_steps()
    
    @Component.listens('OnRefresh')
    def update_pad_steps(self, _ = None):
        self.current_pattern_number = self.fl.patterns.patternNumber()
        self.current_pattern_length = self.fl.patterns.getPatternLength(self.current_pattern_number)
        self.set_selected_channel()
        self.get_pattern_steps()
        colors = self.get_pad_colors(self._current_step_index)
        self.pads.set_lights(colors)

    def get_pattern_steps(self):
        pattern = [] 
        for step_index in range(self.current_pattern_length):
            grid_bit = self.fl.channels.getGridBit(self.selected_channel, step_index)
            pattern.append(grid_bit)
        self.current_pattern_steps = pattern
    
    def set_selected_channel(self):
        self.selected_channel = self.fl.channels.selectedChannel()
        self.set_track_color()

    def set_track_color(self):
        track_color = self.fl.channels.getChannelColor(self.selected_channel)
        b, g, r, a = track_color.to_bytes(4, 'little', signed=True)
        self.track_color = (r,g,b)

    def get_pad_colors(self, current_step_index = -1):
        colors = []
        group_length = 4
        pad_steps_length = len(self.pads._pads)
        self.shift = 0 if current_step_index < pad_steps_length else ( current_step_index // pad_steps_length) * 16

        # Loop over pad number to determine colors for each pad according to the pattern
        for index in range(pad_steps_length):
            step_color_group_index = index // group_length % 2
            shifted_index = index + self.shift
            if shifted_index >= len(self.current_pattern_steps):
                colors.append(self.StepColorState(step_color_group_index, 0))
                continue
            step = self.current_pattern_steps[shifted_index]
            if shifted_index == current_step_index:
                step = 3 if step == 1 else 2
            colors.append(self.StepColorState(step_color_group_index, step))
        return colors

    def activate(self):
        super().activate()
        self.pads.activate()
        self.initialize()

    def deactivate(self):
        super().deactivate()
        self.pads.deactivate()