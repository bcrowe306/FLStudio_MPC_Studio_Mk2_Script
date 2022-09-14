from framework.control_surface import ControlSurface
from .transport import TransportComponent
from .step_sequencer import StepSequencer
from framework.control import Control
from .controls import Controls

class MPCStudioMk2(ControlSurface):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.controls = Controls()
        self.create_components()

    def _create_transport(self):
        self._transport = TransportComponent(
            play_button=self.controls.play_button,
            stop_button=self.controls.stop_button,
            overdub_button=self.controls.overdub_button,
            record_button=self.controls.record_button
        )

    def _create_step_sequencer(self):
        self._step_sequencer = StepSequencer(pads=self.controls.pads_control)

    def create_components(self):
        self._create_transport()
        self._create_step_sequencer()

    def _get_controls(self):
        controls = dict()
        for attr in dir(self.controls):
            control = getattr(self.controls, attr)
            if isinstance(control, Control):
                controls[attr] = control
        return controls

    def deactivate(self):
        super(MPCStudioMk2, self).deactivate()
        for c in self._get_controls():
            c.blackout()