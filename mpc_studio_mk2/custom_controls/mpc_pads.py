from framework.util.event import EventObject
from framework.control import Control
from framework.util.control_map import MidiControlMap
from framework.util.midi import MIDI_STATUS
from framework.util.event import midi_subscribe, midi_unsubscribe
import device

class MPCPad:
    def __init__(self, identifier: int, number: int, name=None, 
    channel: int = 9, playable=False, color: tuple = None, state: str = None, velocity: int = None,
    on_value=1, off_value=0, on_msg_type=MIDI_STATUS.NOTE_ON_CH10, off_msg_type=MIDI_STATUS.NOTE_OFF_CH10
    ) -> None:
        self.identifier: int = identifier
        self.device = device
        self.playable = playable
        self.channel: int = channel
        self.number: int = number
        self.color: tuple = color
        self.state: str = state
        self.velocity: int = velocity
        self.on_value: int = on_value
        self.off_value: int = off_value
        self.on_msg_type: int = on_msg_type
        self.off_msg_type: int = off_msg_type
        
        self.name: int = name or f'mpcpad_{number}_{identifier}'

class MPCPadsControl(Control):
    def __init__(self, name : str, pads: list, pad_sysex_mapping : dict[int, int] =None, default_pad_color : tuple[int, int, int] =None, blackout_color : tuple[int, int, int] = None, *a, **k):
        super().__init__(*a, **k)
        self.default_pad_color = default_pad_color if default_pad_color is not None else (0,0,3)
        self.blackout_color = blackout_color if default_pad_color is not None else (0,0,0)
        self.name = name
        self.mcm = MidiControlMap()
        self.pad_sysex_mapping = pad_sysex_mapping or {
            0:12, 1:13, 2:14, 3:15,
            4:8,  5:9,  6:10, 7:11,
            8:4,  9:5,  10:6, 11:7,
            12:0, 13:1, 14:2, 15:3
        }
        self._pads : list[MPCPad] = []
        self._pads_array = pads
        self._set_pads()

    def set_light(self):
        pass

    def _set_pads(self):
        for i, pad in enumerate(self._pads_array):
            self._pads.append(MPCPad(pad, i))

    def set_lights(self, colors: list):
        pads_to_draw = []
        for index, color in enumerate(colors):
            pad : MPCPad = self._pads[index]
            if pad:
                if pad.color != color:
                    pad.color = color
                    pads_to_draw.append(pad)
        self.draw(pads_to_draw)
        
        
    def draw(self, pads_colors : list[MPCPad]):
        sysex_header = [0xF0, 0x47, 0x47, 0x04A, 0x65, 0x00]
        payload = []
        for pad in pads_colors:
            payload.extend( [ self.pad_sysex_mapping[pad.number], pad.color[0], pad.color[1], pad.color[2] ] )
        length = len(payload)
        sysex_header.append(length)
        sysex_header.extend(payload)
        sysex_header.append(0xF7)
        self.device.midiOutSysex(bytes(sysex_header))
    
    def _on_value(self, event):
        for pad in self._pads:
            if pad.identifier == event.note and event.status == pad.on_msg_type and event.data2 > pad.on_value:
                self._set_step_pressed(pad.number, event)
        self.notify_listeners('value', event)

    def _set_step_pressed(self, step, event):
        self.notify_listeners('step_pressed', step, event)

    def activate(self):
        self.initialize()
        for pad in self._pads:
            midi_subscribe('{}.value'.format(pad.name), self._on_value)
            self.mcm.register_control(pad)

    def deactivate(self):
        for pad in self._pads:
            midi_unsubscribe('{}.value'.format(pad.name), self._on_value)
            self.mcm.unregister_control(pad)
        self.reset()

    def initialize(self):
        self.set_lights(self.generate_global_color_list(self.default_pad_color))
        
    def reset(self):
        self.set_lights(self.generate_global_color_list(self.default_pad_color))

    def blackout(self):
        self.set_lights(self.generate_global_color_list(self.blackout_color))

    def generate_global_color_list(self, color):
        colors = []
        for _ in self._pads:
            colors.append(color)
        return colors