from .control import Control, ControlBase
from .event import GlobalEventObject, EventObject
from .state import StateBase
from .fl_class import FL


class Component(StateBase, EventObject):

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
    
    def __init__(self, auto_active=True, *a, **k):
        super(Component, self).__init__(*a, **k)
        self.name = name
        self.global_event_object = GlobalEventObject()
        self.auto_active = auto_active
        self.fl = FL
        self.state = StateTracker()

    def _control_subscribe(self):
        for attr in dir(self):
            # print(self.name, attr)
            func = getattr(self, attr)
            if hasattr(func, 'control_event') and hasattr(func, 'control_name'):
                # print('{}: {}'.format(self.name, func.__name__))
                control_event = func.control_event
                control_name = func.control_name
                self.global_event_object.subscribe('{}.{}'.format(control_name, control_event), func)

    def _control_unsubscribe(self):
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
                    observers[event_path].append(func)
                else:
                    if func not in self.observers[event_path]:
                        self.observers[event_path].append(func)
        return observers
    
    def _get_controls(self):
        controls = dict()
        for attr in dir(self):
            control = getattr(self, attr)
            if isinstance(control, ControlBase):
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
        if self.isChanged('active', False):
            # Deactivate Controls
            self._control_unsubscribe()
            controls: list[Control] = self._get_controls()
            for control in controls:
                controls[control].deactivate()

            # Unbind listener functions from event_path
            observers = self._get_observers()
            for event_path in observers:
                for func in observers[event_path]:
                    self.global_event_object.unsubscribe(event_path, func)
