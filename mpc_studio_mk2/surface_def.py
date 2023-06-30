class MPCSurfaceDef:
    NOTE_REPEAT=11
    TOUCH_STRIP_BUTTON=0
    PAD_BANK_AE=35	
    PAD_BANK_BF=36
    PAD_BANK_CG=37
    PAD_BANK_DH=38
    FULL_LEVEL=39
    COPY=122
    PAD_MUTE=4
    LEVEL_16=40
    ERASE=9
    SAMPLE_START=33
    SAMPLE_END=34
    SAMPLE_SELECT=42
    MAIN=52
    TC_ON_OFF=15
    AUTOMATION_READ_WRITE=75
    TAP_TEMPO=53
    MODE=114
    QUANTIZE=12
    ZOOM=66
    UNDO=67
    SHIFT=49
    MINUS=55
    PLUS=54
    TUNE=79
    BROWSE=50
    PROGRAM_SELECT=14
    TRACK_SELECT=13
    NUDGE_LEFT=68
    NUDGE_RIGHT=69
    LOCATE=70
    SEEK_BACK=71
    SEEK_FORWARD=72
    RECORD=73
    OVERDUB=80
    STOP=81
    PLAY=82	
    PLAY_START=83
    TOUCH_STRIP=33
    JOG_WHEEL_BUTTON=111
    JOG_WHEEL=100
    JOG_RIGHT_CC_VAL=1
    JOG_LEFT_CC_VAL=127
    TC_LIGHT_1=57
    TC_LIGHT_2=58
    TC_LIGHT_3=59
    TC_LIGHT_4=60
    TC_LIGHT_5=61
    TC_LIGHT_6=62
    TC_LIGHT_7=63
    TC_LIGHT_8=64
    TC_LIGHT_9=65
    TC_1_4=103	
    TC_1_4_T=104	
    TC_1_8=105	
    TC_1_8_T=106	
    TC_1_16=107	
    TC_1_16_T =108	
    TC_1_32=109	
    TC_1_32_T=110
    PAD_0=37
    PAD_1=36
    PAD_2=42
    PAD_3=82
    PAD_4=40
    PAD_5=38
    PAD_6=46
    PAD_7=44
    PAD_8=48
    PAD_9=47
    PAD_10=45
    PAD_11=43
    PAD_12=49
    PAD_13=55
    PAD_14=51
    PAD_15=53
    PAD_MAPPING = {
                37: 0,
                36: 1,
                42: 2,
                82: 3,
                40: 4,
                38: 5,
                46: 6,
                44: 7,
                48: 8,
                47: 9,
                45: 10,
                43: 11,
                49: 12,
                55: 13,
                51: 14,
                53: 15,
            }
    BUTTON_CHANNEL = 0
    PAD_CHANNEL = 9
    PADS_SYSEX_MAP_TOP_DOWN = {
        0: 12, 1: 13, 2: 14, 3: 15,
        4: 8,  5: 9,  6: 10, 7: 11,
        8: 4,  9: 5,  10: 6, 11: 7,
        12: 0, 13: 1, 14: 2, 15: 3
    }
    PADS_ARRANGEMENT = [
    [49, 55, 51, 53],
    [48, 47, 45, 43],
    [40, 38, 46, 44],
    [37, 36, 42, 82]
    ]

    TOTAL_LEDS = 9
    TC_LED_MAPPING = {
        0: 57,
        1: 58,
        2: 59,
        3: 60,
        4: 61,
        5: 62,
        6: 63,
        7: 64,
        8: 65
    }
    REPEAT_LIGHT_MAPPING = {
        7: 110,
        6: 109,
        5: 108,
        4: 107,
        3: 106,
        2: 105,
        1: 104,
        0: 103
    }