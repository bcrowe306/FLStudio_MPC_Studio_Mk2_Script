from util.event import EventObject, notify_listeners
from .component import Component
from util.state import HandleMidiMsg, HandleUIState

class ControlSurface(EventObject):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)

    def OnInit(self):
        self.activate()

    def OnMidiMsg(self, event):
        HandleMidiMsg(event)

    def OnIdle(self):
        HandleUIState()

    def OnUpdateBeatIndicator(self, event):
        notify_listeners('OnUpdateBeatIndicator', event)

    def OnDeInit(self):
        self.deactivate()
    
    def OnRefresh(self, event):
        notify_listeners('OnRefresh', event)

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
