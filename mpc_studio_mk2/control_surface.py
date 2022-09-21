from framework.control_surface import ControlSurface
from framework.modes import Mode, ModesComponent
from .transport import TransportComponent
from .step_sequencer import StepSequencer
from framework.control import Control
from .controls import Controls
from .test_component import TestComponent
from .meters_component import MetersComponent
from surface_def import MPCSurfaceDef as MPC

class MPCStudioMk2(ControlSurface):
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.controls = Controls()
        self.create_components()
        self.create_modes()

    def _create_transport(self):
        self._transport = TransportComponent(
            play_button=self.controls.play_button,
            stop_button=self.controls.stop_button,
            overdub_button=self.controls.overdub_button,
            record_button=self.controls.record_button,
        )

    def _create_step_sequencer(self):
        self._step_sequencer = StepSequencer(pads=self.controls.pads_control, auto_active=False)

    def _create_test_component(self):
        self._test_component = TestComponent(erase_button=self.controls.erase_button, transpose_button=self.controls.full_level, auto_active=False)

    def _create_meters_component(self):
        self._meters_component = MetersComponent(channel=0, led_mapping=MPC.TC_LED_MAPPING, auto_active=False)

    def create_components(self):
        self._create_transport()
        self._create_step_sequencer()
        self._create_test_component()
        self._create_meters_component()

    def create_modes(self):
        self._pad_modes = ModesComponent('pad_modes', default_mode='step_sequencer')
        self._pad_modes.add_mode(Mode('step_sequencer',[self._step_sequencer, self._meters_component], active_color='FULL_2', inactive_color='DIM_1' ) )
        self._pad_modes.add_control('step_sequencer', self.controls.pad_bank_ae)

        self._pad_modes.add_mode(Mode('test_component',[self._test_component], active_color='FULL_2', inactive_color='DIM_1' ) )
        self._pad_modes.add_control('test_component', self.controls.pad_bank_bf)
        
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

