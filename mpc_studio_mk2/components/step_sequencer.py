from framework.component import Component
from mpc_studio_mk2.controls import Controls
from framework.controls.pad_control import PadsControl
from mpc_studio_mk2.surface_def import MPCSurfaceDef as MPC
from mpc_studio_mk2.util import mpc_pad_sysex, mpc_pads_sysex
from framework.util.colors import pad_color

class StepSequencer(Component):
    def __init__(self, name: str, auto_active: bool = True, *a, **k):
        super().__init__(name, auto_active, *a, **k)
        self._current_step_index = -1
        self.current_pattern_steps = None
        self.current_pattern_number = None
        self.current_pattern_length = None
        self.pad_top_down_mapping = MPC.PADS_SYSEX_MAP_TOP_DOWN
        self.shift = 0
        self.selected_step = None
        self.selected_channel = None
        self.track_color = None
        self.hold = False
        params = {
            'pPitch':0,
            'pVelocity':1,
            'pRelease':	2,
            'pFinePitch':3,
            'pPan':	4,
            'pModX':5,
            'pModY'	:6,
            'pShift':7
        }
        self.touch_strip_parameter_mode = params['pPitch']

        # Controls
        self.pads_control = PadsControl(
            name='pads_control',
            channel=MPC.PAD_CHANNEL,
            pad_mapping=MPC.PAD_MAPPING,
            playable=False,
            feedback=None,
            translation=None,
            draw=self.draw_all_pads
        )
        self.erase_button = Controls.erase_button
        self.touch_strip = Controls.touch_strip
        self.touch_strip_button_button = Controls.touch_strip_button_button
        self.led_meter_array = Controls.led_metter_array
        self.led_meter_array.display_volume(.5)

    @Component.listens('OnUpdateMeters')
    def test(self):
        
        if self.hold:
            val = self.GetStepParam(
                self.selected_step, self.touch_strip_parameter_mode)
            unit_value = val / 127
            self.led_meter_array.display_volume(unit_value)
        else: # If a pad is not in held mode, display selected track peak meters
            self.selected_channel = self.fl.channels.selectedChannel()
            linkedTrack = self.fl.channels.getTargetFxTrack(self.selected_channel)
            peak = self.fl.mixer.getTrackPeaks(linkedTrack, 2)
            self.led_meter_array.display_volume(peak)
        
    
    def showGraphEditor(self):
        ch = self.fl.channels
        ch.showGraphEditor(True, self.touch_strip_parameter_mode, self.selected_step, ch.getChannelIndex(
            self.selected_channel), 0)

    @Component.subscribe('touch_strip_button_button', 'pressed')
    def on_touch_strip_button_button_pressed(self, pressed):
        self.touch_strip_button_button.set_light('FULL_1') if pressed else self.touch_strip_button_button.set_light('DIM_1')

    @Component.subscribe('touch_strip_button_button', 'toggled')
    def _on_touch_strip_button_pressed(self, pressed):
        self.touch_strip_parameter_mode = (self.touch_strip_parameter_mode + 1) % 8
        channels = self.fl.channels
        if self.hold:
            self.showGraphEditor() if channels.isGraphEditorVisible() else None
            self.fl.channels.updateGraphEditor()            
        
    @Component.subscribe('touch_strip', 'value')
    def _on_touch_strip_value(self, event_data):
        ch = self.fl.channels

        if self.hold:
            val = self.GetStepParam(self.selected_step, self.touch_strip_parameter_mode)

            # Set Parameter with value form touchstrip
            ch.setStepParameterByIndex(
                self.selected_channel, self.current_pattern_number, self.selected_step, self.touch_strip_parameter_mode, event_data.data2, 1)
            ch.updateGraphEditor()
        else:
            unit_amount = (event_data.data2 / 127)
            self.fl.channels.setChannelVolume(self.fl.channels.selectedChannel(), unit_amount)

    def draw_all_pads(self, pad_colors: list[tuple[int, int, int, int]]):
        sysex = mpc_pads_sysex(pad_colors)
        self.fl.device.midiOutSysex(bytes(sysex))

    def GetStepParam(self, Step, Param):
        return self.fl.channels.getStepParam(Step, Param, 0, 0)
    
    @Component.listens('channels.selectedChannel')
    def on_selected_channel_changed(self, channel):
        if self.isChanged('selected_channel', channel):
            self.selected_channel = self.fl.channels.selectedChannel()
            self.set_track_color()
            self.update_pad_steps()

    def set_track_color(self):
        track_color = self.fl.channels.getChannelColor(self.selected_channel)
        b, g, r, a = track_color.to_bytes(4, 'little', signed=True)
        self.track_color = (r, g, b)

    # Show Graph Editor on pad hold event
    @Component.subscribe('pads_control', 'hold')
    def on_pads_control_hold(self, pad_number, hold):
        self.hold = hold
        ch = self.fl.channels
        
        if hold:
            step_index = self.get_step_from_pad_number(pad_number) + self.shift
            self.selected_step = step_index

            # Make bit be on if it is off
            selected_step_bit = ch.getGridBit(
                self.selected_channel, self.selected_step)
            ch.setGridBit(self.selected_channel, self.selected_step,
                          1) if selected_step_bit == 0 else None
            
            # Show graph Editor
            ch.showGraphEditor(True, self.touch_strip_parameter_mode, step_index, ch.getChannelIndex(
                self.selected_channel), 0)
        else:
            ch.closeGraphEditor(True)


    @Component.subscribe('pads_control', 'short_press')
    def on_pads_control_pad(self, pad_number, event):
        channels = self.fl.channels
        self.selected_step = self.pad_top_down_mapping[pad_number] + self.shift
        selected_step_bit = channels.getGridBit(
            self.selected_channel, self.selected_step)
        channels.setGridBit(self.selected_channel, self.selected_step, 0) if selected_step_bit == 1 else channels.setGridBit(
            self.selected_channel, self.selected_step, 1)

    @Component.listens('mixer.getSongStepPos')
    def _update_pad_led(self, step):
        self._current_step_index = step
        self.update_pad_steps()

    @Component.subscribe('erase_button', 'toggled')
    def _on_erase_button_toggled2(self, toggled):
        print('erase_button: ', toggled)
    
    @Component.listens('patterns.patternNumber')
    def get_current_pattern_number(self, pattern):
        if self.isChanged('pattern', pattern):
            self.get_pattern_info()
            colors = self.get_pad_colors(self._current_step_index)
            self.pads_control.draw(colors)

    def get_pattern_info(self):
        self.current_pattern_number = self.fl.patterns.patternNumber()
        self.current_pattern_length = self.fl.patterns.getPatternLength(
            self.current_pattern_number)
        self.get_pattern_steps()

    def activate(self):
        self.selected_channel = self.fl.channels.selectedChannel()
        self.set_track_color()
        self.update_pad_steps()
        return super().activate()

    @Component.listens('OnRefresh')
    def update_pad_steps(self, _=None):
        self.selected_channel = self.fl.channels.selectedChannel()
        self.get_pattern_info()
        colors = self.get_pad_colors(self._current_step_index)
        self.pads_control.draw(colors)

    def get_pattern_steps(self):
        pattern = []
        for step_index in range(self.current_pattern_length):
            grid_bit = self.fl.channels.getGridBit(
                self.selected_channel, step_index)
            pattern.append(grid_bit)
        self.current_pattern_steps = pattern

    def get_step_from_pad_number(self, pad_number):
        for i in self.pad_top_down_mapping :
            if self.pad_top_down_mapping[i] == pad_number:
                return i
        
    def get_pad_colors(self, current_step_index=-1):
        colors = []
        group_length = 4
        pad_steps_length = len(self.pads_control.pads)
        self.shift = 0 if current_step_index < pad_steps_length else (
            current_step_index // pad_steps_length) * pad_steps_length

        # Loop over pad number to determine colors for each pad according to the pattern
        for index in range(pad_steps_length):
            pad_number = self.pad_top_down_mapping[index]
            step_color_group_index = index // group_length % 2
            shifted_index = index + self.shift
            if shifted_index >= len(self.current_pattern_steps):
                rgb_tuple = self.StepColorState(step_color_group_index, 0)
                colors.append((pad_number, *rgb_tuple))
                continue
            step = self.current_pattern_steps[shifted_index]
            if shifted_index == current_step_index:
                step = 3 if step == 1 else 2
            rgb_tuple = self.StepColorState(step_color_group_index, step)
            colors.append((pad_number, *rgb_tuple))
        return colors
    
    def StepColorState(self, group, step_value):
        r, g, b = self.track_color
        shift = 5
        g = round(g / shift)
        b = round(b / shift)
        group2 = (r, g, b)
        state = {
            0: {
                0: pad_color(self.track_color, 1),
                1: pad_color(self.track_color, 40),
                2: pad_color(self.track_color, 120),
                3: (127, 127, 127)
            },
            1: {
                0: pad_color(group2, 1),
                1: pad_color(group2, 40),
                2: pad_color(group2, 120),
                3: (127, 127, 127)
            }
        }
        return state[group][step_value]
