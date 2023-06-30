from .event import GlobalEventObject
from .util.midi import MIDI_STATUS
from .util.functions import contains, get_index

class ControlRegistry(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ControlRegistry, cls).__new__(
                cls, *args, **kwargs)
        return cls.instance

    def __init__(self) -> None:
        super(ControlRegistry, self).__init__()
        self.event_object = GlobalEventObject()
        self.map = dict()


    def _create_id_tuples(self, control):
        id_list = []
        id_list.append((control.channel, control.identifier, (control.status + control.channel) ))
        if control.status == MIDI_STATUS.NOTE_ON_STATUS:
            id_list.append((control.channel, control.identifier, (control.channel + MIDI_STATUS.NOTE_OFF_STATUS)))
        return id_list


    def register_control(self, control):
        for id_tuple in self._create_id_tuples(control):
            
            if self.map.get(id_tuple) == None:
                self.map[id_tuple] = []
            if not contains(self.map[id_tuple], lambda c: c.name == control.name):
                self.map[id_tuple].insert(0, control)

    def unregister_control(self, control):
        for id_tuple in self._create_id_tuples(control):
            if self.map.get(id_tuple) == None:
                return
            if contains(self.map[id_tuple], lambda c: c.name == control.name):
                c_index = get_index(self.map[id_tuple], control.name)
                del self.map[id_tuple][c_index]

    def HandleMidiMsg(self, event):
        id_tuple = (event.midiChan, event.data1, event.status)
        controls: list = self.map.get(id_tuple)

        # Get the control on the top of the registry stack for this event_it(channel, identifier)
        # Notify the listeners in the event registry and excecute feedback, translation and playable.
        if controls and len(controls) > 0:

            control = controls[0]
            event_id = '{}.{}'.format(control.name, 'value')
            event.handled = not control.playable
            self.event_object.notify_listeners(event_id, event)
            
            if hasattr(control, 'feedback'):
                if hasattr(control.feedback, '__call__'):
                    control.feedback(event, control)

            if hasattr(control, 'translation'):
                if hasattr(control.translation, '__call__'):
                    control.translation(event)

