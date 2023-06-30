from framework.component import Component
from framework.control import ControlBase
from mpc_studio_mk2.controls import Controls


class TransportComponent(Component):

    def __init__(self, *a, **k):
        super(TransportComponent, self).__init__(
            name='TransportComponent', *a, **k)
        self.play_button = Controls.play_button
        self.play_start_button = Controls.play_start_button
        self.stop_button = Controls.stop_button
        self.record_button = Controls.record_button
        self.overdub_button = Controls.overdub_button
        self.nudge_left_button = Controls.nudge_left_button
        self.nudge_right_button = Controls.nudge_right_button
        self.seek_forward_button = Controls.seek_forward_button
        self.seek_back_button = Controls.seek_back_button
        self.locate_button = Controls.locate_button
        self.tap_tempo_button = Controls.tap_tempo_button
        self.undo_button = Controls.undo_button
        self.shift_button = Controls.shift_button
        self.undo_shift_button = Controls.undo_shift_button
        self.tc_on_off_button = Controls.tc_on_off_button
        self.main_button = Controls.main_button

        self.tc_beat_map = {
            0: "Off",
            1: "DIM_2",
            2: "DIM_1"
        }
        self.oc_beat_map = {
            0: "DIM",
            1: "FULL",
            2: "FULL"
        }

    def change_song_position(self, direction: bool):
        delta = .1
        current_pos = self.fl.transport.getSongPos()
        new_pos = current_pos + delta if direction else current_pos - delta 
        self.fl.transport.setSongPos(new_pos)

    @Component.listens('ui.isLoopRecEnabled')
    def _on_isLoopRecEnabled(self, isLoopRecEnabled):
        self.play_start_button.set_light('FULL') if isLoopRecEnabled == 1 else self.play_start_button.set_light('DIM')

    @Component.subscribe('play_start_button', 'toggled')
    def _on_play_start_button_toggled(self, _):
        self.fl.transport.globalTransport(self.fl.midi.FPT_LoopRecord, 1)

    @Component.subscribe('main_button', 'toggled')
    def _on_main_button_toggled(self, _):
        self.fl.transport.setLoopMode()

    @Component.listens('transport.getLoopMode')
    def _on_loop_mode(self, loop_mode):
        if loop_mode == 1:
            self.main_button.set_light('FULL_2')
        else:
            self.main_button.set_light('FULL_1')
    @Component.subscribe('tc_on_off_button', 'toggled')
    def _on_tc_on_off_button_toggled(self, _):
        self.fl.transport.globalTransport(110, 2)

    @Component.listens('ui.isMetronomeEnabled')
    def _set_tc_on_off_button(self, metronome_enabled):
        if metronome_enabled:
            self.tc_on_off_button.set_light('FULL_1')
        else:
            self.tc_on_off_button.set_light('DIM_1')
    @Component.subscribe('undo_shift_button', 'pressed')
    def _on_undo_shift_button_pressed(self, pressed):
        print(pressed)

    @Component.subscribe('undo_button', 'pressed')
    def _on_undo_button_pressed(self, pressed):
        if pressed:
            self.fl.general.undoUp()
            self.undo_button.set_light('FULL_1')
        else:
            self.undo_button.set_light('DIM_1')

    @Component.subscribe('tap_tempo_button', 'pressed')
    def _on_tap_tempo_button_pressed(self, pressed):
        if pressed:
            self.fl.transport.globalTransport(106,1)
            self.tap_tempo_button.set_light('FULL_1')
        else:
            self.tap_tempo_button.set_light('Default')

    @Component.listens('beat')
    def _on_beat(self, beat):
        self.play_button.set_light(self.oc_beat_map[beat])
        
    @Component.subscribe('locate_button', 'pressed')
    def _on_locate_button_pressed(self, pressed):
        if pressed:
            self.locate_button.set_light('FULL')
            self.fl.transport.setSongPos(0.0)
        else:
            self.locate_button.set_light('DIM')

    @Component.subscribe('seek_forward_button', 'pressed')
    def _on_seek_forward_button_pressed(self, pressed):
        if pressed:
            self.seek_forward_button.set_light('FULL')
            self.change_song_position(True)
        else:
            self.seek_forward_button.set_light('DIM')

    @Component.subscribe('seek_back_button', 'pressed')
    def _on_seek_back_button_pressed(self, pressed):
        if pressed:
            self.seek_back_button.set_light('FULL')
            self.change_song_position(False)
        else:
            self.seek_back_button.set_light('DIM')

    @Component.subscribe('nudge_right_button', 'pressed')
    def _on_nudge_right_button_pressed(self, pressed):
        if pressed:
            self.nudge_right_button.set_light('FULL')
            self.fl.transport.fastForward(2,15)
        else:
            self.nudge_right_button.set_light('DIM')
            self.fl.transport.fastForward(0)

    @Component.subscribe('nudge_left_button', 'pressed')
    def _on_nudge_left_button_pressed(self, pressed):
        if pressed:
            self.nudge_left_button.set_light('FULL')
            self.fl.transport.rewind(2,15)
        else:
            self.nudge_left_button.set_light('DIM')
            self.fl.transport.rewind(0)
        

    @Component.subscribe('overdub_button', 'pressed')
    def _on_overdub_button_pressed(self, pressed):
        if pressed:
            value = self.fl.transport.globalTransport(112, 2)

    @Component.subscribe('play_button', 'pressed')
    def _on_play_pressed(self, pressed):
        if pressed:
            self.fl.transport.start()

    @Component.subscribe('stop_button', 'pressed')
    def _on_stop_pressed(self, _):
        self.fl.transport.stop()

    @Component.subscribe('record_button', 'pressed')
    def _on_record_button_pressed(self, pressed):
        if pressed:
            self.fl.transport.record()

    @Component.listens('transport.isRecording')
    def _on_isRecording(self, isRecording):
        if isRecording == 1:
            self.record_button.set_light('FULL')
        else:
            self.record_button.set_light('DIM')

    @Component.listens('transport.isPlaying')
    def on_isPlaying(self, isPlaying):
        if isPlaying == 0:
            self.play_button.set_light('DIM')
            self.stop_button.set_light('FULL')
        else:
            self.play_button.set_light('FULL')
            self.stop_button.set_light('DIM')
