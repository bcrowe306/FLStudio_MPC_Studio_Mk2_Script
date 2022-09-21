from .event import subscriber_map, midi_broadcast, notify_listeners
from .control_map import MidiControlMap
from .fl_class import FL

state_object = {}
midi_state_object = {}
mcm = MidiControlMap()

class StateTracker:
    def __init__(self) -> None:
        self.state_map : dict[str,  dict ] = {}

    def subscribe(self, key, func=None):
        if func is not None and hasattr(func, '__call__'):
            current_state = self.state_map.get(key)
            if current_state is not None:
                subscribers : list = current_state.get('subscribers')
                if subscribers is None:
                    current_state['subsribers'] = []
                if func not in subscribers:
                    subscribers.append(func)
            else:
                self.state_map[key] = {'value': None, 'subscribers': [func]}

    def unsubscribe(self, key, func=None):
        if func is not None and hasattr(func, '__call__'):
            current_state = self.state_map.get(key)
            if current_state is not None:
                subscribers : list = current_state.get('subscribers')
                if subscribers is not None:
                    for f in subscribers:
                        if f == func:
                            subscribers.remove(func)
                            
    def notify(self, key, value):
        current_state_object = self.state_map.get(key)
        if current_state_object is not None:
            if value != current_state_object['value']:
                subscribers: list = current_state_object.get('subscribers')
                if subscribers is not None:
                    for func in subscribers:
                        func(value)
            current_state_object['value'] = value

def HandleMidiMsg(event):
    e = (event.midiChan, event.data1)
    controls = mcm.map.get(e)
    if controls:
        for control in controls:
            event_name = '{}.{}'.format(control.name, 'value')
            midi_broadcast(event_name, event)
            event.handled = not control.playable
            
            if hasattr(control, 'feedback'):
                if hasattr(control.feedback, '__call__'):
                    control.feedback(event, control)

            if hasattr(control, 'translation'):
                if hasattr(control.translation, '__call__'):
                    control.translation(event)

def HandleUIState():
    # Loop through subscriber_map object to find what state we are listening to
    for event_path in subscriber_map:

        # Get the state by the event_path string
        path_list = event_path.split('.')
        if len(path_list) > 1:
            module = getattr(FL, path_list[0])
            new_item_value = getattr(module, path_list[1])()

            # Check to see if we have tracked this state before. If not, state has changed, call all functions subscribed
            if state_object.get(event_path) == None:
                notify_listeners(event_path, new_item_value)
            else:
                # Check to see if state has changed. If so call all subscribed functions with value
                if new_item_value != state_object.get(event_path):
                    notify_listeners(event_path, new_item_value)
            state_object[event_path] = new_item_value
        else:
            if path_list[0] == 'OnIdle':
                notify_listeners(path_list[0], False)