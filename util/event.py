subscriber_map = dict()
midi_subscribers = dict()


def subscribe(event_path, func):
    if subscriber_map.get(event_path) == None:
        subscriber_map[event_path] = []
        subscriber_map[event_path].append(func)
    else:
        if(func not in subscriber_map[event_path]):
            subscriber_map[event_path].append(func)

def unsubscribe(event_path, func):
    handlers = subscriber_map[event_path]
    if handlers == None:
        pass
    else:
        for f in handlers:
            if f == func:
                handlers.remove(func)

def midi_broadcast(event, data):
    if event in midi_subscribers:
        for func in midi_subscribers[event]:
            if hasattr(func, '__call__'):
                func(data)

def midi_subscribe(event_name, func):
    if midi_subscribers.get(event_name) == None:
        midi_subscribers[event_name] = []
        midi_subscribers[event_name].append(func)
    else:
        if(func not in midi_subscribers[event_name]):
            midi_subscribers[event_name].append(func)

def midi_unsubscribe(event_name, func):
    handlers = subscriber_map[event_name]
    if handlers == None:
        pass
    else:
        for f in handlers:
            if f == func:
                handlers.remove(func)

class EventObject(object):
    def __init__(self, *a, **k):
        super(EventObject, self).__init__(*a, **k)
        self._observers = dict()

    def subscribe(self, event, func):
        if self._observers.get(event) == None:
            self._observers[event] = []
            self._observers[event].append(func)
        else:
            if(func not in self._observers[event]):
                self._observers[event].append(func)

    def unsubscribe(self, event_path, func):
        handlers = self._observers[event_path]
        if handlers == None:
            pass
        else:
            for f in handlers:
                if f == func:
                    handlers.remove(func)
    
    def notify_listeners(self, event, *a, **k):
        listeners = self._observers.get(event)
        if listeners != None:
            for func in listeners:
                func(*a, **k)