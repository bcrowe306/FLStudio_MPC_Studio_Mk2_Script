from framework.state import StateBase
from framework.control import ControlBase
import device


class LedMeterArray(StateBase):
    def __init__(self, channel, status, led_array) -> None:
        super().__init__()
        self.status = status
        self.channel = channel
        self.device = device
        self.led_array = led_array
        self.num_segments = len(led_array)


    def generate_pan_meter_led_values(self, volume):
        volume = float(volume) if volume != None else float(0)
        is_positive = False if float(volume) < 0 else True
        vector = 1 if is_positive else -1
        half = self.num_segments // 2
        has_middle = True if self.num_segments % 2 != 0 else False
        led_unit_value = float(round((float(1) / float(half)), 4))
        full_led = abs(int(volume // led_unit_value))
        partial_led_unit_value = round(volume % led_unit_value, 4)
        partial_led = int(
            round(127 * (partial_led_unit_value / led_unit_value)))
        shift = half
        if is_positive and has_middle:
            shift += 1
        if not is_positive:
            shift -= 1
        leds = {}
        for x in range(full_led + 1):
            if x < (full_led):
                leds[x*vector + shift] = 127
            if x == full_led-1 and partial_led != 0:
                leds[x*vector + shift] = partial_led
        led_cc_values = []
        for y in range(self.num_segments):
            if y in leds:
                led_cc_values.append((y, leds[y]))
            else:
                if y == half and has_middle:
                    led_cc_values.append((y, 127))
                else:
                    led_cc_values.append((y, 0))
        return led_cc_values

    # This function generates the necessary cc values for the 9 touch_strip_leds.
    # It accepts a float from 0.0 - 1.0 and will generate a List of tuples with the first item
    # in the tuple being the led index and the second being the CC value
    def generate_led_meter_values(self, volume):

        # Filter out bad input for volume. Volume show be between 0 and 1
        if float(volume) > 1 or float(volume) < 0:
            led_cc_values = []
            for led in range(self.num_segments):
                led_cc_values.append((led, 0))
            return led_cc_values
        else:
            volume = float(volume) if volume != None else float(0)
            led_unit_value = float(
                round((float(1) / float(self.num_segments)), 4))
            full_led_number = int(volume // led_unit_value)
            partial_led_unit_value = round(volume % led_unit_value, 4)
            led_cc_values = []
            for led in range(self.num_segments):
                if led < full_led_number:
                    led_cc_values.append((led, 127))
                if led == full_led_number:
                    cc_value = round(
                        127 * (partial_led_unit_value / led_unit_value))
                    led_cc_values.append((led, int(cc_value)))
                if led > full_led_number:
                    led_cc_values.append((led, 0))
            return led_cc_values
        
    def update_leds(self, led_values):
        for led in led_values:
            led_id = self.led_array[led[0]]
            value = led[1]
            device.midiOutMsg(self.status,
                              self.channel, led_id, value)
            
    def display_volume(self, volume: float):
        if self.isChanged('volume', volume):
            led_values = self.generate_led_meter_values(volume)
            self.update_leds(led_values)


