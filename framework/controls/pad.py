from framework.util.midi import MIDI_STATUS
from framework.controls.button import ButtonControl

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
