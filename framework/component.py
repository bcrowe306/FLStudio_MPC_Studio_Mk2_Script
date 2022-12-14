from framework.util.event import subscribe, unsubscribe
from framework.util.state import StateTracker
from .control import Control
from framework.util.fl_class import FL
class Component(object):

    def listens(*a):
        def dec(func):
            func.event_path = a[0]
            func.custom_args = a[1:]
            return func
        return dec
    
    def subscribe(control_name: str, event: str):
        def dec(func):
            func.control_name = control_name
            func.control_event = event
            return func
        return dec
    
    def __init__(self, auto_active=True, *a, **k):
        super(Component, self).__init__(*a, **k)
        self.auto_active = auto_active
        self.fl = FL
        self.state = StateTracker()

    def _control_subscribe(self):
        controls = self._get_controls()
        for attr in dir(self):
            func = getattr(self, attr)
            if hasattr(func, 'control_event') and hasattr(func, 'control_name'):
                control_event = func.control_event
                control_name = func.control_name
                control = controls.get(control_name)
                if control:
                    control.subscribe(control_event, func)

    def _get_observers(self):
        observers = dict()
        for attr in dir(self):
            func = getattr(self, attr)
            if hasattr(func, 'event_path'):
                event_path = func.event_path
                if observers.get(event_path) == None:
                    observers[event_path] = []
                if func not in observers[event_path]:
                    observers[event_path].append(func)
        return observers
    
    def _get_controls(self) -> dict[str, Control]:
        controls = dict()
        for attr in dir(self):
            control = getattr(self, attr)
            if isinstance(control, Control):
                controls[attr] = control
        return controls

    def activate(self):
        # Activate each control instance of this component
        controls = self._get_controls()
        for control in controls:
            controls[control].activate()
        self._control_subscribe()
        
        # Bind listener functions to event_path in main event loop
        observers = self._get_observers()
        for event_path in observers:
            for func in observers[event_path]:
                subscribe(event_path, func)

    
    def deactivate(self):

        # Deactivate Controls
        controls = self._get_controls()
        for control in controls:
            controls[control].deactivate()

        # Unbind listener functions from event_path
        observers = self._get_observers()
        for event_path in observers:
            for func in observers[event_path]:
                unsubscribe(event_path, func)   