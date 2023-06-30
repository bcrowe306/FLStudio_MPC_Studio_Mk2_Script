def mpc_pad_sysex(pad_number: int, red: int, green: int, blue: int):
    sysex_header = [0xF0, 0x47, 0x47, 0x04A, 0x65, 0x00]
    payload = []
    payload.extend([pad_number, red, green, blue])
    length = len(payload)
    sysex_header.append(length)
    sysex_header.extend(payload)
    sysex_header.append(0xF7)
    return sysex_header

def mpc_pads_sysex(pads_colors: list[tuple[int, int, int,int]]):
    sysex_header = [0xF0, 0x47, 0x47, 0x04A, 0x65, 0x00]
    payload = []
    for pad in pads_colors:
        payload.extend([pad[0],
                        pad[1], pad[2], pad[3]])
    length = len(payload)
    sysex_header.append(length)
    sysex_header.extend(payload)
    sysex_header.append(0xF7)
    return sysex_header

