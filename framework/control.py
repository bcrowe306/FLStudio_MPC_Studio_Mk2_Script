import device
from framework.util.control_map import MidiControlMap
from framework.util.event import EventObject, midi_subscribe, midi_unsubscribe

class Control(EventObject):
    def __init__(self, name=None, channel=None, identifier=None, playable=False, status_type=None,  feedback=None, feedback_process=None, default_color='Default', blackout_color='Off', skin=None):
        super(Control, self).__init__()
        self.device = device
        self._skin = skin
        self.name=name
        self.channel=channel
        self.identifier=identifier
        self.playable=playable
        self.status_type=status_type
        self.feedback=feedback if feedback is not None else feedback
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