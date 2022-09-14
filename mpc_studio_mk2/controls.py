from framework.control import PadControl, ButtonControl, MPCPadsControl
from midi_const import MIDI_STATUS
from surface_def import MPCSurfaceDef as MPC
from color import Skin


def tc_button_control(name, identifier, *a, **k):
        return ButtonControl(
            name, MPC.BUTTON_CHANNEL,
            identifier=identifier, on_value=127, 
            off_value=0, 
            on_msg_type=MIDI_STATUS.NOTE_ON_STATUS, 
            off_msg_type=MIDI_STATUS.NOTE_OFF_STATUS,
            skin=Skin.TwoColorButton,
            *a, **k)
def oc_button_control(name, identifier, *a, **k):
        return ButtonControl(
            name, MPC.BUTTON_CHANNEL,
            identifier=identifier, on_value=127, 
            off_value=0, 
            on_msg_type=MIDI_STATUS.NOTE_ON_STATUS, 
            off_msg_type=MIDI_STATUS.NOTE_OFF_STATUS,
            skin=Skin.OneColorButton,
            *a, **k)
def make_pad_control(identifier, pad_number, *a, **k):
    return PadControl(
        pad_number,
        name=f'pad_{pad_number}',
        channel=MPC.PAD_CHANNEL,
        identifier=identifier,
        on_value=127, 
        off_value=0, 
        on_msg_type=MIDI_STATUS.NOTE_ON_STATUS, 
        off_msg_type=MIDI_STATUS.NOTE_OFF_STATUS,
        skin=Skin.Pad
    )
class Controls:

    def __init__(self) -> None:
        self.play_start_button = oc_button_control('play_start_button', MPC.PLAY_START)
        self.play_button = oc_button_control('play_button', MPC.PLAY)
        self.stop_button = oc_button_control('stop_button', MPC.STOP)
        self.record_button = oc_button_control('record_button', MPC.RECORD)
        self.overdub_button = oc_button_control('overdub_button', MPC.OVERDUB)
        self.mode_button = oc_button_control('mode_button', MPC.MODE)
        self.pads = []
        for pad_id in MPC.PAD_MAPPING:
            pad_number = MPC.PAD_MAPPING[pad_id]
            pad_name = f'pad_{pad_number}'
            setattr(self, pad_name, make_pad_control(pad_id, pad_number))
            self.pads.append(getattr(self, pad_name))
        self.pads_control=MPCPadsControl(name='pads_control', pads=MPC.PAD_STEP_MAPPING)
