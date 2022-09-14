import device
from util.control_map import MidiControlMap
from midi_const import MIDI_STATUS
from util.event import EventObject
from util.event import midi_subscribe, midi_unsubscribe

class Control(EventObject):
    def __init__(self, name, channel, identifier, playable=False, status_type=None,  feedback=False, feedback_process=None, default_color='Default', blackout_color='Off', skin=None):
        super(Control, self).__init__()
        self._skin = skin
        self.name=name
        self.channel=channel
        self.identifier=identifier
        self.playable=playable
        self.status_type=status_type
        self.feedback=feedback
        self.feedback_process=feedback_process
        self.default_color=default_color
        self.blackout_color=blackout_color
        self.mcm = MidiControlMap()

    def _on_value(self, event):
        self.notify_listeners('value', event)

    def activate(self):
        self.initialize()
        midi_subscribe('{}.value'.format(self.name), self._on_value)
        self.mcm.register_control(self)

    def deactivate(self):
        self.reset()
        midi_unsubscribe('{}.value'.format(self.name), self._on_value)
        self.mcm.unregister_control(self)

    def initialize(self):
        self.set_light(self.default_color)
    
    def reset(self):
        self.set_light(self.default_color)

    def blackout(self):
        self.set_light(self.blackout_color)
    
    def set_light(self, value):
        # print(f'Name: {self.name}, value: {value}')
        # try:
            if self._skin:
                color = getattr(self._skin, value)
                color.draw(self)
        # except:
            # print('Skin Color: {}.{} Not found'.format(self._skin, value))

class ButtonControl(Control):
    def __init__(self, name, channel, identifier, button_type='toggle', on_value=127, off_value=0, on_msg_type=MIDI_STATUS.NOTE_ON_STATUS, off_msg_type=MIDI_STATUS.NOTE_OFF_STATUS, *a, **k):
        super(ButtonControl, self).__init__(name, channel, identifier, *a, **k)
        self.button_type = button_type
        self.on_value = on_value
        self.off_value = off_value
        self.on_msg_type = on_msg_type
        self.off_msg_type = off_msg_type
        self._toggled = False
        self._pressed = False
    
    @property
    def isToggled(self):
        return self._toggled

    def _set_toggled(self):
        self._toggled = not self._toggled
        self.notify_listeners('toggled', self._toggled)
        
    @property
    def isPressed(self):
        return self._pressed

    def _set_pressed(self, value):
        self._pressed = value
        self.notify_listeners('pressed', self._pressed)

    def _set_released(self, value):
        self._released = value
        self.notify_listeners('released', self._released)
        
    def _on_value(self, e):
        self.notify_listeners('value', e)
        if e.status == self.on_msg_type and e.data2 == self.on_value:
            self._set_toggled()
            self._set_pressed(e)

        elif e.status == self.off_msg_type and e.data2 == self.off_value:
            self._set_released(e)

class PadControl(ButtonControl):
    def __init__(self, pad_number, *a, **k):
        super().__init__(*a, **k)
        
        self.pad_number = pad_number

    def _on_value(self, e):
        self.notify_listeners('value', e)
        if e.status == self.on_msg_type and e.data2 == self.on_value:
            self._set_toggled()
            self._set_pressed(e)

        elif e.status == self.off_msg_type and e.data2 == self.off_value:
            self._set_released(e)
class MPCPad:
    def __init__(self, identifier: int, number: int, name=None, 
    channel: int = 9, color: tuple = None, state: str = None, velocity: int = None,
    on_value=1, off_value=0, on_msg_type=MIDI_STATUS.NOTE_ON_CH10, off_msg_type=MIDI_STATUS.NOTE_OFF_CH10
    ) -> None:
        self.identifier: int = identifier
        self.playable = False
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

class MPCPadsControl(EventObject):
    def __init__(self, name, pads: list, pad_sysex_mapping=None, *a, **k):
        super().__init__(*a, **k)
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
        device.midiOutSysex(bytes(sysex_header))
    
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
        pass
    def initialize(self):
        pass
    def reset(self):
        pass
    def blackout(self):
        pass
