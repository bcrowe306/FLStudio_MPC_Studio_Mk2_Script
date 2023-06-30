from framework.util.midi import MIDI_STATUS
from framework.controls.button import ButtonControl
from framework.controls.combo_control import ComboControl
from framework.controls.jog_control import JogControl
from framework.controls.slider_control import SliderControl
from framework.visual.led_meter_array import LedMeterArray
from .surface_def import MPCSurfaceDef as MPC
from framework.util.midi import MIDI_STATUS

from .skin import Skin

def tc_button_control(name, identifier, *a, **k):
    return ButtonControl(
        name=name,
        channel=MPC.BUTTON_CHANNEL,
        identifier=identifier,
        status=MIDI_STATUS.NOTE_ON_STATUS,
        on_value=127,
        off_value=0,
        on_msg_type=MIDI_STATUS.NOTE_ON_STATUS,
        off_msg_type=MIDI_STATUS.NOTE_OFF_STATUS,
        skin=Skin.TwoColorButton,
        *a, **k)


def oc_button_control(name, identifier, *a, **k):
    return ButtonControl(
        name, MPC.BUTTON_CHANNEL,
        identifier=identifier, 
        on_value=127,
        off_value=0,
        on_msg_type=MIDI_STATUS.NOTE_ON_STATUS,
        off_msg_type=MIDI_STATUS.NOTE_OFF_STATUS,
        skin=Skin.OneColorButton,
        *a, **k)
def combo_button_control(name, primary_button: ButtonControl, modifier_button: ButtonControl ):
    pass

class Controls:

    
    play_start_button = oc_button_control('play_start_button', MPC.PLAY_START)
    play_button = oc_button_control('play_button', MPC.PLAY)
    stop_button = oc_button_control('stop_button', MPC.STOP)
    record_button = oc_button_control('record_button', MPC.RECORD)
    overdub_button = oc_button_control('overdub_button', MPC.OVERDUB)

    nudge_left_button = oc_button_control('nudge_left_button', MPC.NUDGE_LEFT)
    nudge_right_button = oc_button_control('nudge_right_button', MPC.NUDGE_RIGHT)
    seek_forward_button = oc_button_control(
        'seek_forward_button', MPC.NUDGE_RIGHT)
    locate_button = oc_button_control('locate_button', MPC.LOCATE)
    seek_back_button = oc_button_control('seek_back_button', MPC.SEEK_BACK)
    seek_forward_button = oc_button_control(
        'seek_forward_button', MPC.SEEK_FORWARD)

    main_button = tc_button_control('main_button', MPC.MAIN)
    tc_on_off_button = tc_button_control('tc_on_off_button', MPC.TC_ON_OFF)
    automation_read_write_button = tc_button_control('automation_read_write_button', MPC.AUTOMATION_READ_WRITE)
    tap_tempo_button = tc_button_control('tap_tempo_button', MPC.TAP_TEMPO)
    
    mode_button = tc_button_control('mode_button', MPC.MODE)
    quantize_button = tc_button_control('quantize_button', MPC.QUANTIZE)
    zoom_button = tc_button_control('zoom_button', MPC.ZOOM)
    undo_button = tc_button_control('undo_button', MPC.UNDO)

    shift_button = tc_button_control('shift_button', MPC.SHIFT)
    minus_button = tc_button_control('minus_button', MPC.MINUS)
    plus_button = tc_button_control('plus_button', MPC.PLUS)
    tune_button = tc_button_control('tune_button', MPC.TUNE)

    track_select_button = tc_button_control('track_select_button', MPC.TRACK_SELECT)
    program_select_button = tc_button_control('program_select_button', MPC.PROGRAM_SELECT)
    browse_button = tc_button_control('browse_button', MPC.BROWSE)

    sample_select_button = tc_button_control('sample_select_button', MPC.SAMPLE_SELECT)
    sample_start_button = tc_button_control('sample_start_button', MPC.SAMPLE_START)
    sample_end_button = tc_button_control('sample_end_button', MPC.SAMPLE_END)

    note_repeat_button = tc_button_control('note_repeat_button', MPC.NOTE_REPEAT)
    touch_strip_button_button = tc_button_control('touch_strip_button_button', MPC.TOUCH_STRIP_BUTTON)
    pad_bank_ae = tc_button_control('pad_bank_ae', MPC.PAD_BANK_AE)
    pad_bank_bf = tc_button_control('pad_bank_bf', MPC.PAD_BANK_BF)
    pad_bank_cg = tc_button_control('pad_bank_cg', MPC.PAD_BANK_CG)
    pad_bank_dh = tc_button_control('pad_bank_dh', MPC.PAD_BANK_DH)
    full_level_button = tc_button_control('full_level_button', MPC.FULL_LEVEL)
    copy_button = tc_button_control('copy_button', MPC.COPY)
    pad_mute_button = tc_button_control('pad_mute_button', MPC.PAD_MUTE)
    level_16_button = tc_button_control('level_16_button', MPC.LEVEL_16)
    erase_button = tc_button_control('erase_button', MPC.ERASE)

    touch_strip = SliderControl('touch_strip', channel=0, identifier=MPC.TOUCH_STRIP)

    jog_wheel = JogControl(name='jog_wheel', channel=0, identifier=MPC.JOG_WHEEL, status=MIDI_STATUS.CC_STATUS)
    jog_button = oc_button_control('jog_button', MPC.JOG_WHEEL_BUTTON)
    
    # Shift Controls
    undo_shift_button = ComboControl('undo_shift_button', undo_button, shift_button)
    jog_wheel_shift = ComboControl('jog_wheel_shift', primary_control=jog_wheel, modifier_button=shift_button)
    jog_shift_button = ComboControl('jog_shift_button', jog_button, shift_button)

    # Visual Controls
    led_metter_array = LedMeterArray(MPC.BUTTON_CHANNEL, MIDI_STATUS.CC_STATUS, MPC.TC_LED_MAPPING)

