from util.control_map import MidiControlMap
from midi_const import MIDI_STATUS
from util.event import EventObject
from util.event import midi_subscribe, midi_unsubscribe

def control_event(event_name):

    def event_decorator(self):

        def event_listener_decorator(event_listener):
            self.subscribe[event_name] = event_listener
            return self

        return event_listener_decorator

    def event_setter(self, event_listener):
        self.subscribe[event_name] = event_listener

    return property(event_decorator, event_setter)


class Control(EventObject):
    value = control_event('value')
    def __init__(self, name, channel, identifier, playable=False, status_type=None,  feedback=False, feedback_process=None, default_color='Default', skin=None):
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
        self.set_light('Off')

    def set_light(self, value):
        try:
            if self._skin:
                color = getattr(self._skin, value)
                color.draw(self)
        except:
            print('Skin Color: {}.{} Not found'.format(self._skin, value))

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
        
    def _on_value(self, e):
        self.notify_listeners('value', e)
        if e.status == self.on_msg_type and e.data2 == self.on_value:
            self._set_toggled()
            self._set_pressed(True)

        elif e.status == self.off_msg_type and e.data2 == self.off_value:
            self._set_pressed(True)