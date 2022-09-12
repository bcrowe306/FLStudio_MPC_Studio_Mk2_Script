from util.event import subscribe, unsubscribe
from .control import Control
class Component(object):

    def listens(event_path: str):
        def dec(func):
            func.event_path = event_path
            return func
        return dec
    
    def subscribe(control_name: str, event: str):
        def dec(func):
            func.control_name = control_name
            func.control_event = event
            return func
        return dec
    
    def __init__(self, *a, **k):
        super(Component, self).__init__(*a, **k)

    def _control_subscribe(self):
        controls = self._get_controls()
        for attr in dir(self):
            func = getattr(self, attr)
            if hasattr(func, 'control_event') and hasattr(func, 'control_name'):
                control_event = func.control_event
                control_name = func.control_name
                controls[control_name].subscribe(control_event, func)

    def _get_observers(self):
        observers = dict()
        for attr in dir(self):
            func = getattr(self, attr)
            if hasattr(func, 'event_path'):
                event_path = func.event_path
                if observers.get(event_path) == None:
                    observers[event_path] = []
                    observers[event_path].append(func)
                else:
                    if func not in self.observers[event_path]:
                        self.observers[event_path].append(func)
        return observers
    
    def _get_controls(self):
        controls = dict()
        for attr in dir(self):
            control = getattr(self, attr)
            if isinstance(control, Control):
                controls[attr] = control
        return controls

    def activate(self):

        # Activate each control instance of this component
        self._control_subscribe()
        controls = self._get_controls()
        for control in controls:
            controls[control].activate()
        
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