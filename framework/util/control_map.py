def contains(list, filter):
    for x in list:
        if filter(x):
            return True
    return False

def get_index(list, name):
    for index, item in enumerate(list):
        if item.name == name:
            return index
    else:
        return -1
    
class MidiControlMap(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(MidiControlMap, cls).__new__(cls, *args, **kwargs)
        return cls.instance
    def __init__(self) -> None:
        super(MidiControlMap, self).__init__()
        self.map = dict()
    
    def register_control(self, control):
        id_tuple = ( control.channel, control.identifier )
        if self.map.get(id_tuple) == None:
            self.map[id_tuple] = []
        if not contains(self.map[id_tuple], lambda c: c.name == control.name):
            self.map[id_tuple].append(control)

    def unregister_control(self, control):
        id_tuple = ( control.channel, control.identifier )
        if self.map.get(id_tuple) == None:
            return
        if contains(self.map[id_tuple], lambda c: c.name == control.name):
            c_index = get_index(self.map[id_tuple], control.name)
            del self.map[id_tuple][c_index]
