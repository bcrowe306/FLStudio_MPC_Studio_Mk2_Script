from util.event import subscribe, unsubscribe

class Component:
    def __init__(self):
        self.observers = dict()
        self.controls = []

    def add_listener(self, event_path, func):
        if self.observers.get(event_path) == None:
            self.observers[event_path] = []
            self.observers[event_path].append(func)
        else:
            if func not in self.observers[event_path]:
                self.observers[event_path].append(func)

    def activate(self):
        for control in self.controls:
            control.activate()
        for event_path in self.observers:
            for func in self.observers[event_path]:
                subscribe(event_path, func)

    def add_control(self, control):
        self.controls.append(control)

    def remove_control(self, control):
        self.controls.remove(control)

    def deactivate(self):
        for control in self.controls:
            control.deactivate()
        for event_path in self.observers:
            for func in self.observers[event_path]:
                unsubscribe(event_path, func)