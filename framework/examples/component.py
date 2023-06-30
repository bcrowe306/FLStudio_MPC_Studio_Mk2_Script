from framework.component import Component

class NewComponent(Component):
    def __init__(self, name: str, auto_active: bool = True, *a, **k):
        super().__init__(name, auto_active, *a, **k)
        