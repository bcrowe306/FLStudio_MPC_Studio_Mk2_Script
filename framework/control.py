from framework.control_registry import ControlRegistry
from .util.midi import MIDI_STATUS
from framework.event import EventObject, GlobalEventObject
from framework.state import StateBase
import device
def control_event(event_name):

    def event_decorator(self):

        def event_listener_decorator(event_listener):
            self.subscribe[event_name] = event_listener
            return self

        return event_listener_decorator

    def event_setter(self, event_listener):
        self.subscribe[event_name] = event_listener

    return property(event_decorator, event_setter)


class ControlBase(EventObject, StateBase):
    def __init__(self, name: str, channel: int, identifier: int, status=MIDI_STATUS.NOTE_ON_STATUS, playable=False, *a, **k):
        super(ControlBase, self).__init__(*a, **k)
        self.name = name
        self.channel = channel
        self.identifier = identifier
        self.status = status
        self.playable = playable
        self.device = device
        self.event_object = GlobalEventObject()
        self.registry = ControlRegistry()

    def notify(self, event_name: str, *a, **k):
        self.event_object.notify_listeners(
            '{}.{}'.format(self.name, event_name), *a, **k)
            
    def activate(self):
        pass
    def deactivate(self):
        pass
    def _on_value(self, event):
        pass
    def reset(self):
        pass
    def blackout(self):
        pass


class Control(ControlBase):
    value = control_event('value')
    def __init__(self, name, channel, identifier, playable=False, status=MIDI_STATUS.NOTE_ON_STATUS,  feedback=False, feedback_process=None, default_color='Default', blackout_color='Off', skin=None):
        super(Control, self).__init__(name, channel, identifier, status, playable)
        self._skin = skin
        self.feedback=feedback
        self.feedback_process=feedback_process
        self.default_color=default_color
        self.blackout_color=blackout_color

    def _on_value(self, event):
        self.notify_listeners('value', event)
        pass

    def activate(self):
        self._initialize()
        self.event_object.subscribe('{}.value'.format(self.name), self._on_value)        
        self.registry.register_control(self)

    def deactivate(self):
        self.reset()
        self.event_object.unsubscribe('{}.value'.format(self.name), self._on_value)
        self.registry.unregister_control(self)

    def _initialize(self):
        self.set_light(self.default_color)
    
    def reset(self):
        self.set_light(self.default_color)

    def blackout(self):
        self.set_light(self.blackout_color)
    
    def set_light(self, value, *a, **k):
        try:
            if self._skin:
                color = getattr(self._skin, value)
                color.draw(self, *a, **k)
        except:
            print('Skin Color: {}.{} Not found'.format(self._skin, value))
