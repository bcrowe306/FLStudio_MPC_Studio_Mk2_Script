import playlist, channels, transport, mixer, patterns, arrangement, ui, plugins, general, midi, device

class FL:
    playlist = playlist
    channels = channels
    transport = transport
    mixer = mixer
    patterns = patterns
    arrangement = arrangement
    ui = ui
    plugins = plugins
    general = general
    midi = midi
    device = device

class flMidiMsg:
    handled:bool
    status:int
    data1:int
    data2:int
    port:int
    note:int
    velocity:int
    pressure:int
    progNum:int
    controlNum:int
    controlVal:int
    pitchBend:int
    sysex:bytes
    isIncrement:bool
    res:float
    inEv:int
    outEv:int
    midiId:int
    midiChan:int
    midiChanEx:int
    pmeFlags:int
