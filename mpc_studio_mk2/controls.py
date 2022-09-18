from framework.controls.button import ButtonControl
from framework.controls.pad import PadControl
from framework.control import Control
from .custom_controls.mpc_pads import MPCPadsControl
from framework.util.midi import MIDI_STATUS
from surface_def import MPCSurfaceDef as MPC
from color import Skin
from framework.util.colors import pad_color

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
def pad_feedback(event, control: Control):
    brightness = event.data2
    color=(50,149,77)
    new_color_tuple = pad_color(color, brightness)
    red, green, blue = new_color_tuple
    current_color = getattr(control, 'current_color', None)
    if new_color_tuple != current_color or current_color == None:
        control.device.midiOutSysex(bytes([0xF0, 0x47, 0x47, 0x04A, 0x65, 0x00, 0x04, 0, red, green, blue, 0xF7]))
        setattr(control, 'current_color', color)


def make_pad_control2(identifier, pad_number, name, *a, **k):
    return PadControl(
        pad_number,
        name=name,
        channel=MPC.PAD_CHANNEL,
        identifier=identifier,
        on_value=127, 
        off_value=0, 
        on_msg_type=MIDI_STATUS.NOTE_ON_STATUS, 
        off_msg_type=MIDI_STATUS.NOTE_OFF_STATUS,
        skin=Skin.Pad,
        feedback=pad_feedback,
        playable=True
    )

class Controls:

    def __init__(self) -> None:
        self.play_start_button = oc_button_control('play_start_button', MPC.PLAY_START)
        self.play_button = oc_button_control('play_button', MPC.PLAY)
        self.stop_button = oc_button_control('stop_button', MPC.STOP)
        self.record_button = oc_button_control('record_button', MPC.RECORD)
        self.overdub_button = oc_button_control('overdub_button', MPC.OVERDUB)
        self.mode_button = oc_button_control('mode_button', MPC.MODE)
        self.erase_button = oc_button_control('erase_button', MPC.ERASE)
        self.pad_bank_ae = tc_button_control('pad_bank_ae', MPC.PAD_BANK_AE)
        self.pad_bank_bf = tc_button_control('pad_bank_bf', MPC.PAD_BANK_BF)
        self.pad_bank_cg = tc_button_control('pad_bank_cg', MPC.PAD_BANK_CG)
        self.pad_bank_dh = tc_button_control('pad_bank_dh', MPC.PAD_BANK_DH)
        self.pad_00 = make_pad_control2(MPC.PAD_0, 0, 'pad_00')
        self.pads = []
        for pad_id in MPC.PAD_MAPPING:
            pad_number = MPC.PAD_MAPPING[pad_id]
            pad_name = f'pad_{pad_number}'
            setattr(self, pad_name, make_pad_control(pad_id, pad_number))
            self.pads.append(getattr(self, pad_name))
        self.pads_control=MPCPadsControl(name='pads_control', pads=MPC.PAD_STEP_MAPPING, default_pad_color=(0,0,0))
