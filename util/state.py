from .event import subscriber_map, midi_broadcast
from .control_map import MidiControlMap
from .fl_class import FL

fl = FL()

state_object = {}
midi_state_object = {}
mcm = MidiControlMap()


def HandleMidiMsg(event):
    e = (event.midiChan, event.data1)
    controls = mcm.map.get(e)
    if controls:
        for c in controls:
            event_name = '{}.{}'.format(c.name, 'value')
            midi_broadcast(event_name, event)
            event.handled = not c.playable
                

def HandleUIState():
    # Loop through subscriber_map object to find what state we are listening to
    for event_path in subscriber_map:

        # Get the state by the event_path string
        path_list = event_path.split('.')
        module = getattr(fl, path_list[0])
        new_item_value = getattr(module, path_list[1])()

        # Check to see if we have tracked this state before. If not, state has changed, call all functions subscribed
        if state_object.get(event_path) == None:
            for f in subscriber_map[event_path]:
                f(new_item_value)
        else:
            # Check to see if state has changed. If so call all subscribed functions with value
            if new_item_value != state_object.get(event_path):
                for f in subscriber_map[event_path]:
                    f(new_item_value)
        state_object[event_path] = new_item_value