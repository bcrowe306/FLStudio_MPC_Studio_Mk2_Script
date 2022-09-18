from framework.util.control_map import MidiControlMap
from framework.control import Control
class PadsControl(Control):
    def __init__(self, name : str, pads: list, channel :int, playable=True, initial_note :int =24, default_pad_color : tuple[int, int, int] =None, blackout_color : tuple[int, int, int] = None, *a, **k):
        super().__init__(*a, **k)
        self.default_pad_color = default_pad_color if default_pad_color is not None else (0,0,3)
        self.blackout_color = blackout_color if default_pad_color is not None else (0,0,0)
        self.name = name
        self._pads = pads

    def set_light(self):
        pass
    
    def _on_value(self, event):
        for pad in self._pads:
            if pad.identifier == event.note and event.status == pad.on_msg_type and event.data2 > pad.on_value:
                self._set_step_pressed(pad.number, event)
        self.notify_listeners('value', event)

    def _set_step_pressed(self, step, event):
        self.notify_listeners('step_pressed', step, event)

    def activate(self):
        for pad in self._pads:
            midi_subscribe('{}.value'.format(pad.name), self._on_value)
            self.mcm.register_control(pad)
        self.initialize()

    def deactivate(self):
        for pad in self._pads:
            midi_unsubscribe('{}.value'.format(pad.name), self._on_value)
            self.mcm.unregister_control(pad)

    def initialize(self):
        self.set_lights(self.generate_global_color_list(self.default_pad_color))
        
    def reset(self):
        self.set_lights(self.generate_global_color_list(self.default_pad_color))

    def blackout(self):
        self.set_lights(self.generate_global_color_list(self.blackout_color))

    def generate_global_color_list(self, color):
        colors = []
        for _ in self._pads:
            colors.append(color)
        return colors