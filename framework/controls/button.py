from framework.util.midi import MIDI_STATUS
from framework.control import Control

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
