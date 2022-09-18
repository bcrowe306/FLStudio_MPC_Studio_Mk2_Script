from framework.component import Component
from framework.controls.button import ButtonControl
from framework.controls.pad import PadControl

class TestComponent(Component):
    def __init__(self, erase_button : ButtonControl, pad_00 : PadControl, auto_active=True, *a, **k):
        super().__init__(auto_active, *a, **k)
        self.erase_button : ButtonControl = erase_button
        self.pad_00 : PadControl = pad_00

        @Component.subscribe('erase_button', 'pressed')
        def print_value(self, value):