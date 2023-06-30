from framework.util.midi import MIDI_STATUS
from framework.fl_class import flMidiMsg
from framework.control import Control



class ButtonControl(Control):
    def pressed(control_name: str, event: str):
        def dec(func):
            func.control_name = control_name
            func.control_event = event
            return func
        return dec
    @staticmethod
    def generate_button_events(on_msg_status: int, off_msg_status: int, event_data: flMidiMsg) -> dict[str: any]:
        events: dict[str: any] = dict()
        if event_data.status == on_msg_status:
            events['toggled'] = None
            events['pressed'] = True

        elif event_data.status == off_msg_status:
            events['pressed'] = False
            events['released'] = True
        return events
        
    def __init__(
        self, name, channel, identifier,
        playable=False,
        status=MIDI_STATUS.NOTE_ON_STATUS,
        feedback=False, 
        feedback_process=None, 
        default_color='Default', 
        blackout_color='Off', 
        skin=None,
        on_value=127, 
        off_value=0, 
        on_msg_type=MIDI_STATUS.NOTE_ON_STATUS, 
        off_msg_type=MIDI_STATUS.NOTE_OFF_STATUS, 
        hold_time=10, *a, **k):
        super().__init__(name, channel, identifier, playable, status,
                         feedback, feedback_process, default_color, blackout_color, skin)
        self.on_value = on_value
        self.off_value = off_value
        self.on_msg_type = on_msg_type
        self.off_msg_type = off_msg_type
        self._toggled = False
        self._pressed = False
        self._hold = False
        self._hold_counter = 0
        self.hold_time = hold_time
        

    @property
    def isToggled(self):
        return self._toggled


    def _on_idle(self):
        pass
        if self._pressed:
          self.hold_counter += 1
          if self.hold_counter > self.hold_time:
            if self.isChanged('_hold', True):
                self._set_hold(True)
        else:
            self.hold_counter = 0
            if self.isChanged('_hold', False):
                self._set_hold(False)


    def _set_hold(self, hold):
        self._hold = hold
        self.notify('hold', self._hold)

    @property
    def isHold(self) -> bool:
        return self._hold

    def activate(self):
        self.event_object.subscribe('idle', self._on_idle)
        return super().activate()

    @property
    def isPressed(self) -> bool:
        return self._pressed
        
    def _set_toggled(self):
        self._toggled = not self._toggled
        self.notify('toggled', self._toggled)

    def _set_pressed(self, value):
        self._pressed = value
        self.notify('pressed', self._pressed)

    def _set_released(self, value):
        self._released = value
        self.notify('released', self._released)

    def _on_value(self, event_data):
        events = ButtonControl.generate_button_events(self.on_msg_type, self.off_msg_type, event_data)
        for event in events:
            setattr(self, '_{}'.format(event), events[event])
            self.notify(event, events[event])
