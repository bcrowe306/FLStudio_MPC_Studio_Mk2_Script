def rgb_to_hsv(r, g, b):
    maxc = max(r, g, b)
    minc = min(r, g, b)
    v = maxc
    if minc == maxc:
        return 0.0, 0.0, v
    s = (maxc-minc) / maxc
    rc = (maxc-r) / (maxc-minc)
    gc = (maxc-g) / (maxc-minc)
    bc = (maxc-b) / (maxc-minc)
    if r == maxc:
        h = bc-gc
    elif g == maxc:
        h = 2.0+rc-bc
    else:
        h = 4.0+gc-rc
    h = (h/6.0) % 1.0
    return h, s, v


def hsv_to_rgb(h, s, v):
    if s == 0.0:
        return v, v, v
    i = int(h*6.0)  # XXX assume int() truncates!
    f = (h*6.0) - i
    p = v*(1.0 - s)
    q = v*(1.0 - s*f)
    t = v*(1.0 - s*(1.0-f))
    i = i % 6
    if i == 0:
        return v, t, p
    if i == 1:
        return q, v, p
    if i == 2:
        return p, v, t
    if i == 3:
        return p, q, v
    if i == 4:
        return t, p, v
    if i == 5:
        return v, p, q


def pad_color(rgc_255_tuple: tuple[int, int, int], brightness: int = 5, min: int = 2, max: int = 110):
    r, g, b = rgc_255_tuple
    if brightness > max:
        brightness = max
    elif brightness < min:
        brightness = min
    unit_color = (r/255, g/255, b/255)
    hsv = rgb_to_hsv(*unit_color)
    new_color_unit = hsv_to_rgb(hsv[0], hsv[0], brightness/127)
    red, green, blue = new_color_unit
    red = round(red * 127)
    green = round(green * 127)
    blue = round(blue * 127)
    return (red, green, blue)
