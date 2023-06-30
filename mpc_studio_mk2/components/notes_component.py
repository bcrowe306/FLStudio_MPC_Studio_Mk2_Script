from framework.component import Component
from mpc_studio_mk2.surface_def import MPCSurfaceDef as MPC
from framework.controls.pad_control import PadsControl
from mpc_studio_mk2.controls import Controls
from framework.util.colors import pad_color
from framework.util.scales import Scales
from mpc_studio_mk2.util import mpc_pad_sysex, mpc_pads_sysex

class NotesComponent(Component):
    def __init__(self, name: str = 'notes_component', auto_active: bool = True, *a, **k):
        super().__init__(name, auto_active, *a, **k)
        self.name = name
        self.color = (50, 149, 77)
        self.root_color = (254, 10, 77)
        self.off_color = (0, 0, 0)
        self.shift = 48
        self.full_level = False
        self.octave_colors = [
            (50, 149, 77),
            (149, 77, 50),
            (77, 50, 149),
            (150, 0, 149),
            (0, 150, 149),
            (150, 150, 0),
            (60, 5, 100),
            (100, 5, 40),
            (10, 50, 150),
            (40, 150, 0),
        ]
        self.Scales = [Scales.chromatic, Scales.major, Scales.minor, Scales.melodic, Scales.harmonic, Scales.pentatonic]
        self.scale = None
        self.pads_control = PadsControl(
            name='pads_control',
            channel=MPC.PAD_CHANNEL,
            pad_mapping=MPC.PAD_MAPPING,
            playable=True,
            feedback=self.pad_feedback,
            translation=self.translation,
            draw=self.draw_all_pads
        )
        self.copy_button = Controls.copy_button
        self.erase_button = Controls.erase_button
        self.level_16_button = Controls.level_16_button
        self.full_level_button = Controls.full_level_button

    def set_shift(self, shift):
        self.shift += shift
        self.pads_control.draw(self.generate_pad_colors())

    @Component.listens('pads_component.full_level')
    def on_full_level_change(self):
        self.full_level_button.set_light('DIM_1') if self.full_level else self.full_level_button.set_light('FULL_2')

    @Component.subscribe('full_level_button', 'toggled')
    def toggle_full_level(self, _):
        self.notify('full_level')
        self.full_level = not self.full_level

    @Component.subscribe('level_16_button', 'pressed')
    def on_level_16_button_pressed(self, pressed):
        self.level_16_button.set_light(
            'FULL_1') if pressed else self.level_16_button.set_light('DIM_1')

    @Component.subscribe('level_16_button', 'toggled')
    def on_level_16_button_toggled(self, _):
        self.set_shift(12)

    @Component.subscribe('erase_button', 'pressed')
    def on_erase_button_pressed(self, pressed):

        self.erase_button.set_light(
            'FULL_1') if pressed else self.erase_button.set_light('DIM_1')

    @Component.subscribe('erase_button', 'toggled')
    def on_erase_button_toggled(self, _):
        self.set_shift(-12)

    @Component.subscribe('copy_button', 'toggled')
    def _on_copy_button_toggled(self, _):
        self.rotate_scale()

    @Component.subscribe('copy_button', 'pressed')
    def _on_copy_button_pressed(self, pressed):
        self.copy_button.set_light('FULL_1') if pressed else self.copy_button.set_light('DIM_1')

    def set_scale(self, scale_index):
        self._state['scale_index'] = scale_index
        self.scale = self.Scales[scale_index]
        self.notify('scale', self.scale)
        self.pads_control.draw(self.generate_pad_colors())
    
    def rotate_scale(self):
        new_scale_index = ( self._state['scale_index'] + 1 ) % len(self.Scales)
        self.set_scale(new_scale_index)

    @Component.subscribe('pads_control', 'pad')
    def test(self, pad_number, event):
        pass

    @Component.listens('channels.selectedChannel')
    def on_selected_channel(self, channel):
        # if self.isChanged('selectedChannel', channel):
        #     print(self.fl.channels.getChannelColor(channel))
        pass

    def translation(self, midi_event):
        midi_event.data2 = 127 if self.full_level else midi_event.data2
        pad_index = self.pads_control.pad_mapping[midi_event.data1]
        scale_degree = self.scale[pad_index % len(self.scale)] + (12 * (pad_index // len(self.scale)))
        new_note = scale_degree + self.shift
        midi_event.data1 = new_note

    def activate(self):
        self.set_scale(0)
        super().activate()

    def deactivate(self):
        self.pads_control.draw(self.generate_off_colors())
        super().deactivate()

    def draw_all_pads(self, pad_colors: list[tuple[int, int, int, int]]):
        sysex = mpc_pads_sysex(pad_colors)
        self.fl.device.midiOutSysex(bytes(sysex))

    def generate_pad_colors(self):
        pad_colors = []
        color = self.octave_colors[self.shift // 12]
        brightness=5
        for pad_id in self.pads_control.pad_mapping:
            pad_index = self.pads_control.pad_mapping[pad_id]
            new_color_tuple = pad_color(self.root_color, brightness) if pad_index % len(
                self.scale) == 0 else pad_color(color, brightness)
            pad_colors.append(
                (pad_index, new_color_tuple[0], new_color_tuple[1], new_color_tuple[2]))
        return pad_colors

    def generate_off_colors(self):
        pad_colors = []
        brightness=0
        for pad_id in self.pads_control.pad_mapping:
            pad_index = self.pads_control.pad_mapping[pad_id]
            new_color_tuple = pad_color(self.off_color, brightness) if pad_index % len(
                self.scale) == 0 else pad_color(self.off_color, brightness)
            pad_colors.append(
                (pad_index, new_color_tuple[0], new_color_tuple[1], new_color_tuple[2]))
        return pad_colors

    def pad_feedback(self, event, control):
        brightness = event.data2
        color = self.octave_colors[self.shift // 12]
        new_color_tuple = pad_color(self.root_color, brightness) if control.number % len(self.scale) == 0 else pad_color(color, brightness)
        red, green, blue = new_color_tuple
        if control.isChanged('color', new_color_tuple):
            sysex = mpc_pad_sysex(control.number, red, green, blue)
            control.device.midiOutSysex(bytes(sysex))
