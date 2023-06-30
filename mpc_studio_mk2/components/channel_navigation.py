from framework.component import Component
from mpc_studio_mk2.controls import Controls

class ChannelNavigationComponent(Component):
    def __init__(self, name: str = 'ChannelNavigationComponent'):
        super(ChannelNavigationComponent, self).__init__(name=name)
        self.jog_wheel = Controls.jog_wheel
        self.jog_button = Controls.jog_button
        self.selected_channel = None
        self.sample_select_button = Controls.sample_select_button
        self.sample_start_button = Controls.sample_start_button
        self.sample_end_button = Controls.sample_end_button
        self.minus_button = Controls.minus_button
        self.plus_button = Controls.plus_button
        self.jog_wheel_shift = Controls.jog_wheel_shift
        

    @Component.subscribe('minus_button', 'toggled')
    def _on_minus_button_toggled(self, _):
        ui = self.fl.ui
        self.fl.ui.setFocused(1)
        self.fl.ui.right()
   

    @Component.subscribe('plus_button', 'toggled')
    def _on_plus_button_toggled(self, _):
        ui = self.fl.ui
        self.fl.ui.setFocused(1)
        self.fl.ui.left()

    @Component.subscribe('jog_wheel_shift', 'jogged')
    def _on_jog_wheel_shift_jogged(self, jogged):
        print(jogged)

    @Component.subscribe('sample_start_button', 'pressed')
    def _on_sample_start_button_pressed(self, pressed):
        self.sample_start_button.set_light(
            'FULL_1') if pressed else self.sample_start_button.set_light('DIM_1')

    @Component.subscribe('sample_start_button', 'toggled')
    def _on_sample_start_button_toggled(self, toggled):
        if self.fl.patterns.patternNumber() < self.fl.patterns.patternMax():
            self.fl.patterns.jumpToPattern(self.fl.patterns.patternNumber() + 1)

    @Component.subscribe('sample_end_button', 'pressed')
    def _on_sample_end_button_pressed(self, pressed):
        self.sample_end_button.set_light(
            'FULL_1') if pressed else self.sample_end_button.set_light('DIM_1')

            
    @Component.subscribe('sample_end_button', 'toggled')
    def _on_sample_end_button_toggled(self, toggled):
        if self.fl.patterns.patternNumber() > 1:
            self.fl.patterns.jumpToPattern(self.fl.patterns.patternNumber() - 1)

    @Component.subscribe('sample_select_button', 'toggled')
    def _on_sample_select_toggled(self, _):
        self.fl.channels.muteChannel(self.fl.channels.selectedChannel())
        self.set_muted_lights()

    def set_muted_lights(self):
        muted = self.fl.channels.isChannelMuted(
            self.fl.channels.selectedChannel())
        if muted:
            self.sample_select_button.set_light("FULL_2")
        else:
            self.sample_select_button.set_light("FULL_1")
    @Component.subscribe('jog_button', 'toggled')
    def _on_jog_button_toggled(self, _):
        self.fl.channels.showCSForm(self.selected_channel, -1)

    @Component.subscribe('jog_wheel', 'jogged')
    def _on_jog_wheel_jogged(self, value):
        channel_length = self.fl.channels.channelCount()
        next_index = 0
        if value:
            next_index = self.selected_channel + \
                1 if self.selected_channel + 1 < channel_length else 0
        else:
            next_index = self.selected_channel - \
                1 if self.selected_channel - 1 >= 0 else channel_length - 1
        self.fl.channels.selectOneChannel(next_index)
        self.set_muted_lights()

    @Component.listens('channels.selectedChannel')
    def set_selected_channel(self, channel):
        self.selected_channel = channel

    def activate(self):
        super().activate()
        self.set_muted_lights()

