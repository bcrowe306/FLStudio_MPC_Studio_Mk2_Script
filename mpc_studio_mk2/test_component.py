from framework.component import Component
from framework.controls.button import ButtonControl
from framework.controls.pad import PadControl
from framework.control import Control
from framework.midi_event import flMidiEvent
from mpc_studio_mk2.custom_controls.mpc_pads import MPCPad
from framework.util.event import midi_subscribe, midi_unsubscribe
from surface_def import MPCSurfaceDef
from framework.util.colors import pad_color

class PlayPads(Control):
    def __init__(self, pads_mapping, *a, **k):
        super().__init__(*a, **k)
        self._pads_mapping : dict[int, int] = pads_mapping
        self._pads : dict[int, MPCPad] = {}
        self.shift = 48
        self._set_pads()
    
    def pad_feedback(self, event, control: Control):
        brightness = event.data2
        color=(50,149,77)
        new_color_tuple = pad_color(color, brightness)
        red, green, blue = new_color_tuple
        current_color = getattr(control, 'current_color', None)
        if new_color_tuple != current_color or current_color == None:
            control.device.midiOutSysex(bytes([0xF0, 0x47, 0x47, 0x04A, 0x65, 0x00, 0x04, control.number, red, green, blue, 0xF7]))
            setattr(control, 'current_color', color)

    def translation(self, midi_event : flMidiEvent):
        new_note = self._pads[midi_event.data1].number + self.shift
        midi_event.data1 = new_note
        print(new_note)
    
    def _set_pads(self):
        for id, new_note_arrangement in self._pads_mapping.items():
            self._pads[id] = MPCPad(id, new_note_arrangement, playable=True)
            
    def _on_value(self, value):
        pass

    def activate(self):
        print('here')
        
        for _, pad in self._pads.items():
            setattr(pad, 'translation', self.translation)
            setattr(pad, 'feedback', self.pad_feedback)

            midi_subscribe('{}.value'.format(pad.name), self._on_value)
            self.mcm.register_control(pad)

    def deactivate(self):
        for _, pad in self._pads.items():
            midi_unsubscribe('{}.value'.format(pad.name), self._on_value)
            self.mcm.unregister_control(pad)
        self.reset()


class TestComponent(Component):
    def __init__(self, erase_button : ButtonControl, transpose_button : PadControl, auto_active=True, *a, **k):
        super().__init__(auto_active, *a, **k)
        self.erase_butto : ButtonControl = erase_button
        self.transpose_button : ButtonControl = transpose_button
        # self.pad_00 : PadControl = pad_00
        self.play_pads = PlayPads(pads_mapping=MPCSurfaceDef.PAD_MAPPING)

    @Component.subscribe('transpose_button', 'pressed')
    def print_value(self, value):
        self.play_pads.shift += 12