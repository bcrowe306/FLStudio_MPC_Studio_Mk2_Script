from framework.control import Control
from midi_const import MIDI_STATUS

class JogControl(Control):
    def __init__(self, name, channel, identifier, inc_value, dec_value, jog_msg_type=MIDI_STATUS.CC_STATUS, playable=False, status_type=None, feedback=False, feedback_process=None, default_color='Default', blackout_color='Off', skin=None):
        super().__init__(name, channel, identifier, playable, status_type, feedback, feedback_process, default_color, blackout_color, skin)
        self.inc_value = inc_value
        self.dec_value = dec_value
        self.jog_msg_type = jog_msg_type
    
    def _on_value(self, e):
        self.notify_listeners('value', e)
        if e.status == self.jog_msg_type:
            value = True if e.data2 == self.inc_value else False
            self._set_jogged(value)

    def _set_jogged(self, value):
        self.notify_listeners('jogged', value)