import device
from framework.util.control_map import MidiControlMap
from framework.util.event import EventObject
from framework.util.event import midi_subscribe, midi_unsubscribe

class VisualControl(EventObject):
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
        
    def activate(self):
        self.initialize()

    def deactivate(self):
        self.reset()

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