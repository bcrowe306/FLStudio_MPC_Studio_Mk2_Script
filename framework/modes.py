from control import Control
from component import Component
from util.event import EventObject

class Mode(EventObject):
    def __init__(self, name: str, components: list[Component],  *a, **k):
        super().__init__(*a, **k)
        self.name = name
        self.components = components or []
    
    def activate(self):
        for component in self.components:
            component.activate()

    def deactivate(self):
        for component in self.components:
            component.deactivate()

class ModesComponent(Component):
    def __init__(self, name: str, controls: list[tuple(str, Control, str)], cycle_control: Control = None, default_mode: str =None, *a, **k):
        super().__init__(*a, **k)
        self.name = name
        self.controls = controls
        self.cycle_control = cycle_control
        self.default_mode = default_mode
        self._active_mode: Mode = None
        self._previous_mode: Mode = None
        self.modes: dict[str, Mode]
    
    
    def set_active_mode(self, mode_name: str):
        if self._active_mode:
            self._active_mode.deactivate()
            self._previous_mode = self._active_mode
        self._active_mode = self.modes[mode_name]
        self._active_mode.activate()

    def _generate_activation_function(self, mode_name):
        def _set_active_mode():
            if self._active_mode:
                self._active_mode.deactivate()
                self._previous_mode = self._active_mode
            self._active_mode = self.modes[mode_name]
            self._active_mode.activate()
        return _set_active_mode
            
    def activate(self):
        for control_tuple in self.controls:
            control: Control =  control_tuple[1]
            control.subscribe(control_tuple[2], self._generate_activation_function(control_tuple[0]))
        if self.default_mode:
            self.set_active_mode(self.default_mode)
        super(ModesComponent, self).activate()
        
    def deactivate(self):
        for control_tuple in self.controls:
            control: Control =  control_tuple[1]
            control.unsubscribe(control_tuple[2], self._generate_activation_function(control_tuple[0]))
        if self._active_mode:
            self._active_mode.deactivate()
        super(ModesComponent, self).deactivate()
        

    