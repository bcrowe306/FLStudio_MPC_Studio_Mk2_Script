from framework.component import Component
from framework.control import ButtonControl
from util.fl_class import FL

class TransportComponent(Component):
    def __init__(self, 
        play_button: ButtonControl = None, 
        stop_button: ButtonControl = None, 
        record_button: ButtonControl = None, 
        overdub_button: ButtonControl = None, 
        metronome_button: ButtonControl = None, 
        *a, **k):
        super(TransportComponent, self).__init__(*a, **k)
        self.play_button: ButtonControl = play_button
        self.stop_button: ButtonControl = stop_button
        self.record_button: ButtonControl = record_button
        self.overdub_button: ButtonControl = overdub_button
        self.metronome_button: ButtonControl = metronome_button

    @Component.subscribe('play_button', 'pressed')
    def _on_play_button_toggled(self, value):
        FL.transport.stop() if FL.transport.isPlaying() else FL.transport.start()

    @Component.subscribe('stop_button', 'pressed')
    def _on_stop_button_toggled(self, _):
        FL.transport.stop() 
    
    @Component.listens('transport.isPlaying')
    def _on_transport_isPlaying(self, isPlaying):
            if isinstance(self.play_button, ButtonControl):
                self.play_button.set_light('FULL') if isPlaying else self.play_button.set_light('DIM')
            if isinstance(self.stop_button, ButtonControl):
                self.stop_button.set_light('DIM') if isPlaying else self.stop_button.set_light('FULL')

    @Component.listens('transport.isRecording')
    def _on_transport_isRecording(self, isRecording):
            if isinstance(self.record_button, ButtonControl):
                self.record_button.set_light('FULL') if isRecording else self.record_button.set_light('DIM')

    @Component.subscribe('record_button', 'pressed')
    def _on_record_button_pressed(self, _):
        FL.transport.record() 
        
    @Component.subscribe('overdub_button', 'pressed')
    def _on_overdub_button_pressed(self, _):
        FL.transport.globalTransport(112, 1) 