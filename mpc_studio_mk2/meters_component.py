from framework.component import Component
from framework.util.midi import MIDI_STATUS as mi
from surface_def import MPCSurfaceDef as MPC
import device
class MetersComponent(Component):
    def __init__(self, channel=None, status_type=None, led_mapping=None, auto_active=True, *a, **k):
        super().__init__(auto_active, *a, **k)
        self.led_mapping = led_mapping if led_mapping is not None else []
        self.status_type = status_type if status_type is not None else mi.CC_STATUS
        self.channel = channel if channel is not None else 0
        self.selected_channel = None

    def get_meter_values(self, value) -> list[tuple]:
        leds = len(self.led_mapping)
        led_values = []
        full_leds = value * (leds * 127) //  127
        partial_led = round( value * (leds * 127) %  127 )
        for l in range(leds):
            led = self.led_mapping[l]
            if l < full_leds:
                led_values.append((led, 127))
            elif l == full_leds and partial_led != 0:
                led_values.append((led, partial_led))
            else:
                led_values.append((led,0))
        return led_values
    
    def draw_leds(self, value):
        if value <= 1:
            led_values = self.get_meter_values(value)
            for led in led_values:
                id, cc_value = led
                # print(f'{id}, {cc_value}')
                device.midiOutMsg(mi.CC_STATUS, self.channel, id, cc_value)

    
    @Component.listens('OnRefresh')
    def set_selected_channel(self, _=None):
        self.selected_channel = self.fl.channels.selectedChannel() + 1

    @Component.listens('OnIdle')
    def _get_track_peaks(self, event):
        if self.selected_channel is not None:
            peak = self.fl.mixer.getTrackPeaks(self.selected_channel,2)
            self.state.notify(f'track', round(peak, 2))
    
    def initialize(self):
        self.set_selected_channel()
        self.state.subscribe(f'track', self.draw_leds)

    def activate(self):
        super().activate()
        self.initialize()

    def deactivate(self):
        super().deactivate()
        self.draw_leds(0)

    