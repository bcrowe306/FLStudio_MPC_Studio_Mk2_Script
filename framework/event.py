from .fl_class import FL
fl = FL()

class EventObject(object):
    def __init__(self, *a, **k):
        super(EventObject, self).__init__(*a, **k)
        self.observers = dict()

    def subscribe(self, event_id: str, func):
        if self.observers.get(event_id) == None:
            self.observers[event_id] = []
        if(func not in self.observers[event_id]):
            self.observers[event_id].append(func)
        # if event_id == 'erase_button.pressed':
        #     for f in self.observers[event_id]:
        #         print(f.__name__)

    def unsubscribe(self, event_id: str, func):
        handlers: list = self.observers[event_id]
        if handlers != None:
            for f in handlers:
                if f == func:
                    handlers.remove(f)
    
    def notify_listeners(self, event_id: str, *a, **k):
        _listeners = self.observers.get(event_id)
        if _listeners != None:
            for func in _listeners:
                if hasattr(func, '__call__'):
                    func(*a, **k)

class GlobalEventObject(EventObject):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(GlobalEventObject, cls).__new__(
                cls, *args, **kwargs)
        return cls.instance

    def __init__(self) -> None:
        super(GlobalEventObject, self).__init__()
