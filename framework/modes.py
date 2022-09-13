from .control import Control
from .component import Component
from util.event import EventObject

class Mode(EventObject):
    def __init__(self, name: str, components: list[Component], active_color='Default', inactive_color='Off',  *a, **k):
        super().__init__(*a, **k)
        self.name = name
        self.active_color = active_color
        self.inactive_color = inactive_color
        self.components = components or []
    
    def activate(self):
        for component in self.components:
            component.activate()

    def deactivate(self):
        for component in self.components:
            component.deactivate()

class ModesComponent(Component):
    def __init__(self, name: str, cycle_control: Control = None, default_mode: str =None, *a, **k):
        super(ModesComponent, self).__init__(*a, **k)
        self.name = name
        self.cycle_control = cycle_control
        self.default_mode = default_mode
        self._controls = dict()
        self._active_mode: Mode = None
        self._previous_mode: Mode = None
        self.modes: dict[str, Mode] = {}
    
    def add_mode(self, mode, behavior='default'):
        self.modes[mode.name] = mode
    
    def add_control(self, mode_name, control, event_name='pressed'):
        self._controls[mode_name] = (control, event_name)
    
    def _get_ctrl_from_mode_name(self, mode_name):
        control_tuple = self._controls.get(mode_name)
        if control_tuple:
            return control_tuple[0]

    def set_active_mode(self, mode_name: str):
        if self._active_mode:
            self._active_mode.deactivate()
            control: Control = self._get_ctrl_from_mode_name(self._active_mode.name)
            control.set_light(self._active_mode.inactive_color)
            self._previous_mode = self._active_mode
        self._active_mode = self.modes[mode_name]
        self._active_mode.activate()
        control: Control = self._get_ctrl_from_mode_name(mode_name)
        control.set_light(self._active_mode.active_color)
    def _generate_activation_function(self, mode_name):
        def _set_active_mode(*_, **__):
            if self._active_mode:
                self._active_mode.deactivate()
                control: Control = self._get_ctrl_from_mode_name(
                    self._active_mode.name)
                control.set_light(self._active_mode.inactive_color)
                self._previous_mode = self._active_mode
            self._active_mode = self.modes[mode_name]
            self._active_mode.activate()
            control: Control = self._get_ctrl_from_mode_name(mode_name)
            control.set_light(self._active_mode.active_color)
        return _set_active_mode
            
    def activate(self):
        for mode_name in self._controls:
            control_tuple = self._controls[mode_name]
            control: Control = control_tuple[0]
            event_name = control_tuple[1]
            control.subscribe(
                event_name, self._generate_activation_function(mode_name))
            setattr(self, control.name, control)
        if self.default_mode:
            self.set_active_mode(self.default_mode)
        super(ModesComponent, self).activate()
        
    def deactivate(self):
        for mode_name in self._controls:
            control_tuple = self._controls[mode_name]
            control: Control = control_tuple[0]
            event_name = control_tuple[1]
            control.unsubscribe(
                event_name, self._generate_activation_function(mode_name))
        if self._active_mode:
            self._active_mode.deactivate()
        super(ModesComponent, self).deactivate()
