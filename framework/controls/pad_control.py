from framework.control import Control
from framework.util.midi import MIDI_STATUS
from framework.event import EventObject, GlobalEventObject
from framework.state import StateBase
from framework.control_registry import ControlRegistry
from framework.control import ControlBase
from framework.util.colors import pad_color
class cc(ControlBase):
    def __init__(self, name: str, channel: int, identifier: int, status=MIDI_STATUS.NOTE_ON_STATUS, playable=False, *a, **k):
        super().__init__(name, channel, identifier, status, playable, *a, **k)


class PadControl(ControlBase):
    def __init__(self, name, channel, identifier, 
    number: int,
    color: tuple = None,
    playable=False, 
    on_msg_type: int = MIDI_STATUS.NOTE_ON_STATUS,
    off_msg_type: int = MIDI_STATUS.NOTE_OFF_STATUS,
    feedback=None, 
    translation=None
    ):
        
        self.name: str = name or f'pad_{number}_{identifier}'
        self.identifier: int = identifier
        self.playable = playable
        self.channel: int = channel
        self.number: int = number
        self.color: tuple = color
        # self.velocity: int = velocity
        self.status = on_msg_type
        self.on_msg_type: int = on_msg_type
        self.off_msg_type: int = off_msg_type
        self.feedback = feedback
        self.translation = translation
        super().__init__(self.name, channel, identifier, on_msg_type, playable,)

    def set_light(self, *a, **k):
        if hasattr(self.draw, '__call__'):
            self.draw(self, *a, **k)

class PadsControl(ControlBase):
    def __init__(self, name: str, channel: int, pad_mapping: dict[int: int], on_msg_type: int = MIDI_STATUS.NOTE_ON_STATUS,
                 off_msg_type: int = MIDI_STATUS.NOTE_OFF_STATUS, hold_time=10, short_press_time=5, playable=True, feedback=None, translation=None, draw=None):

        self.event_object: GlobalEventObject = GlobalEventObject()
        self.registry: ControlRegistry = ControlRegistry()
        self.name: str = name
        self.channel: int = channel
        self.on_msg_type: int = on_msg_type
        self.off_msg_type: int = off_msg_type
        self.pad_mapping: dict[int: int] = pad_mapping
        self.playable = playable
        self.feedback = feedback
        self.translation = translation
        self.draw = draw
        self.shift = 24
        self.pads: list[PadControl] = []
        self.hold_time = hold_time
        self.short_press_time = short_press_time
        self.pad_state = dict()
        for pad_id in self.pad_mapping:
            pad_number = self.pad_mapping[pad_id]
            self.pad_state[pad_number] = dict()
            self.pad_state[pad_number]['hold_counter'] = 0
            self.pad_state[pad_number]['hold'] = False
            self.pads.append(self.__generate_pad_control(pad_id))

    def _pad_state_is_changed(self, pad_number, event_name, value):
        changed = False
        current_state = self.pad_state[pad_number].get(event_name)
        if current_state == None:
            changed = True
            self.pad_state[pad_number][event_name] = value
        else:
            if value != current_state:
                changed = True
        self.pad_state[pad_number][event_name] = value
        return changed
    
    def get_pad_event_state(self, pad_number, event_name):
        return self.pad_state[pad_number].get(event_name)
    
    def set_pad_event_state(self, pad_number, event_name, value):
        self.pad_state[pad_number][event_name] = value
    
    def _on_idle(self):
        for pad_number in self.pad_state:
            if self.get_pad_event_state(pad_number, 'pressed'):
                self.pad_state[pad_number]['hold_counter'] += 1
                if self.pad_state[pad_number]['hold_counter'] > self.hold_time:
                    if self._pad_state_is_changed(pad_number, 'hold', True):
                        self._set_hold(pad_number, True)
            else:
                self.pad_state[pad_number]['hold_counter'] = 0
                if self._pad_state_is_changed(pad_number, 'hold', False):
                    self._set_hold(pad_number, False)

    def _set_hold(self, pad_number, hold):
        self.notify('hold', pad_number, hold)     

    def _set_pressed(self, pad_number: int, pressed: bool, event):
        self.set_pad_event_state(pad_number, 'pressed', pressed)
        self.notify('pressed', pad_number, pressed, event)

    def _set_released(self, pad_number: int, released: bool, event):
        hold_counter = self.pad_state[pad_number]['hold_counter']
        if hold_counter > 0 and hold_counter < self.short_press_time:
            self.notify('short_press', pad_number, True)
        self.set_pad_event_state(pad_number, 'released', released)
        self.notify('released', pad_number, released, event)

    def _on_value(self, event):
        self.notify('value', event)
        pad_number = self.pad_mapping[event.data1]
        self.notify('pad', pad_number, event)
        if event.status == (self.on_msg_type + self.channel):
            self.notify('toggled', pad_number, event)
            self._set_pressed(pad_number, True, event)
        elif event.status == (self.off_msg_type + self.channel):
            self._set_pressed(pad_number, False, event)
            self._set_released(pad_number, True, event)

    def __generate_pad_control(self, pad_id):
        pad_name = '{}_{}_{}'.format(
            self.name, self.pad_mapping[pad_id], pad_id)
        return PadControl(
            # Template = [control_name]_pad_[pad_number]_[midi_id]
            name=pad_name,
            channel=self.channel,
            identifier=pad_id,
            on_msg_type= self.on_msg_type,
            off_msg_type=self.off_msg_type,
            number=self.pad_mapping[pad_id],
            playable=self.playable,
            translation=self.translation,
            feedback=self.feedback,
        )
    
    def activate(self):
        self.event_object.subscribe('idle', self._on_idle)
        for pad in self.pads:
            self.event_object.subscribe('{}.value'.format(pad.name), self._on_value)
            self.registry.register_control(pad)

    def deactivate(self):
        for pad in self.pads:
            self.event_object.unsubscribe('{}.value'.format(pad.name), self._on_value)
            self.registry.unregister_control(pad)

    def _initialize(self):
        self.set_light(self.default_color)

    def reset(self):
        self.set_light(self.default_color)

    def blackout(self):
        self.set_light(self.blackout_color)
