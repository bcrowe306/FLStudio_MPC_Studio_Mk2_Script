from .event import EventObject
from .util.functions import safe_getattr
from .fl_class import FL

class StateBase():
    def __init__(self) -> None:
        self._state = dict()

    def isChanged(self, state: str, value: any) -> bool:
        changed = False
        current_state = self._state.get(state)
        if current_state == None:
            changed = True
            self._state[state] = value
        else:
            if value != current_state:
                changed = True
        self._state[state] = value
        return changed

class StateObject(object):
    def __init__(self, event_object: EventObject) -> None:
        super(StateObject, self).__init__()
        self.event_object = event_object
        self.state = dict()

    def HandleState(self, event_id: str, value: any):
        if self.state.get(event_id) == None:
            self.event_object.notify_listeners(event_id, value)
        else:
            if value != self.state.get(event_id):
                self.event_object.notify_listeners(event_id, value)
        self.state[event_id] = value


class UIState(StateObject):
    def __init__(self, event_object: EventObject) -> None:
        super(UIState, self).__init__(event_object)
        self.fl = FL

    def HandleState(self):
        # Loop through subscriber_map object to find what state we are listening to
        self.event_object.notify_listeners('idle')
        for event_id in self.event_object.observers:

            # Get the state by the event_id string
            path_list = event_id.split('.')

            # This checks to see if this event_id is for the UI state.
            module = safe_getattr(self.fl, path_list[0])
            if module != None: 
                new_state = getattr(module, path_list[1])()
                # Check to see if we have tracked this state before. If not, state has changed, call all functions subscribed
                old_state = self.state.get(event_id)
                if old_state == None:
                    self.event_object.notify_listeners(event_id, new_state)
                else:
                    # Check to see if state has changed. If so call all subscribed functions with value
                    if new_state != old_state:
                        self.event_object.notify_listeners(
                            event_id, new_state)
                self.state[event_id] = new_state