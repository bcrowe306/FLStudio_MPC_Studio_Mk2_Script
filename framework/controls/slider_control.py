from framework.control import Control
from framework.util.midi import MIDI_STATUS

class SliderControl(Control):
    def __init__(self, name: str, channel: int, identifier: int, status: int = MIDI_STATUS.CC_STATUS, playable=False, feedback=False, feedback_process=None, default_color='Default', blackout_color='Off', skin=None):
        super().__init__(name, channel, identifier, playable, status,
                         feedback, feedback_process, default_color, blackout_color, skin)

    def _on_value(self, e):
        pass
        # self.notify('value', e)
    
