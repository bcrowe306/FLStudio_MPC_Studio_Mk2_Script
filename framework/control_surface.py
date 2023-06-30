from .event import GlobalEventObject, EventObject
from .component import Component
from .control_registry import ControlRegistry
from .state import UIState
import device

class ControlSurface(EventObject):
    def __init__(self, has_meters: bool = False, *a, **k):
        super().__init__(*a, **k)
        self.has_meters = has_meters
        self.global_event_object = GlobalEventObject()
        self.control_registry = ControlRegistry()
        self.ui_state = UIState(self.global_event_object)

    def OnInit(self):
        device.setHasMeters() if self.has_meters else None
        self.activate()

    def OnMidiMsg(self, event):
        self.control_registry.HandleMidiMsg(event)

    def OnIdle(self):
        self.ui_state.HandleState()

    def OnUpdateBeatIndicator(self, event):
        self.global_event_object.notify_listeners('beat', event)

    def OnDeInit(self):
        self.deactivate()

    def OnRefresh(self, event):
        self.global_event_object.notify_listeners('OnRefresh', event)

    def OnUpdateMeters(self):
        self.global_event_object.notify_listeners('OnUpdateMeters')
        
    def _get_components(self):
        components = dict()
        for attr in dir(self):
            component = getattr(self, attr)
            if isinstance(component, Component):
                components[attr] = component
        return components

    def activate(self):
        components = self._get_components()
        for component in components:
            if components[component].auto_active:
                components[component].activate()

    def deactivate(self):
        components = self._get_components()
        for component in components:
            components[component].deactivate()
