from framework.control import ControlBase, Control
from framework.fl_class import flMidiMsg
from framework.util.midi import MIDI_STATUS
from .button import ButtonControl
from .jog_control import JogControl
from .slider_control import SliderControl
class CC(ControlBase):
    def __init__(self, name: str, channel: int, identifier: int, status=MIDI_STATUS.NOTE_ON_STATUS, playable=False, *a, **k):
        super().__init__(name, channel, identifier, status, playable, *a, **k)

class ComboControl(ControlBase):
    def __init__(self, 
    name: str,
    primary_control: Control,
    modifier_button: ButtonControl,
    modifier_button_event: str = 'pressed', *a, **k):

        super(ComboControl, self).__init__(name, modifier_button.channel, modifier_button.identifier, status=primary_control.status, *a, **k)
        self.name: str = name
        self.channel: int = primary_control.channel
        self.identifier: int = primary_control.identifier
        self.primary_control: Control = primary_control
        self.modifier_button: ButtonControl = modifier_button
        self.modifier_button_event: str = modifier_button_event
        self._toggled: bool = False
        self._pressed: bool = False
        self._hold: bool = False
        self._hold_counter: int = 0
        self.hold_time: int = 10

    def _on_modifier_button_event(self, event_data):
        if event_data:
            self.registry.register_control(self)
        else:
            self.registry.unregister_control(self)

    def _set_jogged(self, value):
        self.notify('jogged', value)
        self.notify('inc', value) if value else self.notify('dec', value)

    def _on_modified_primary_value(self, event_data: flMidiMsg):
        if isinstance(self.primary_control, JogControl):
            events = JogControl.generate_jog_events(
                self.primary_control.status, self.primary_control.inc_value, self.primary_control.dec_value, event_data)
            for event in events:
                self.notify(event, events[event])

        elif isinstance(self.primary_control, ButtonControl):
            button_events = ButtonControl.generate_button_events(
                self.primary_control.on_msg_type, self.primary_control.off_msg_type, event_data)
            for event in button_events:
                setattr(self, '_{}'.format(event), button_events[event])
                self.notify(event, button_events[event])

        elif isinstance(self.primary_control, SliderControl):
            pass

    def activate(self):
        self.modifier_button.activate()
        self.event_object.subscribe('{}.{}'.format(self.name, 'value'), self._on_modified_primary_value)
        self.event_object.subscribe('{}.{}'.format(self.modifier_button.name, self.modifier_button_event), self._on_modifier_button_event)
    
        
