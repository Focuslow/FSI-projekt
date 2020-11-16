import math


def accel0(t1, t2, m1, m2, l1, l2, g, v1, v2):
    up1 = -g * (2 * m1 + m2) * math.sin(t1) - m2 * g * math.sin(t1 - 2 * t2)
    up2 = -2 * math.sin(t1 - t2) * m2 * ((v2 * v2) * l2 + (v1 * v1) * l1 * math.cos(t1 - t2))

    up = up1 + up2
    down = l1 * (2 * m1 + m2 - m2 * math.cos(2 * t1 - 2 * t2))

    return float(up / down)


def accel1(t1, t2, m1, m2, l1, l2, g, v1, v2):
    up1 = 2 * math.sin(t1 - t2)
    up2 = (v1 * v1) * l1 * (m1 + m2) + g * (m1 + m2) * math.cos(t1) + (v2 * v2) * l2 * m2 * math.cos(t1 - t2)

    up = up1 * up2
    down = l2 * (2 * m1 + m2 - m2 * math.cos(2 * t1 - 2 * t2))

    return float(up / down)


def angles(x0, y0, l0, x1, y1, l1):
    # get triangle 0
    sidex0 = l0 + x0
    sidey0 = -y0
    if sidex0 == 0:
        if y0 > 0:
            new_angle0 = -math.pi
        else:
            new_angle0 = math.pi
    else:
        new_angle0 = math.atan2(sidey0, sidex0) + math.pi / 2
        if sidey0==0:
            if sidex0<0:
                new_angle0 = - math.pi / 2
    new_len0 = math.sqrt(sidex0 ** 2 + sidey0 ** 2)

    # get triangle 1
    sidex1 = l1 + x1 -x0
    sidey1 = -y1 +y0
    if sidex1 == 0:
        if sidey1 > 0:
            new_angle1 = math.pi
        else:
            new_angle1 = 0

    elif sidex1<0:
        new_angle1 = math.pi - math.atan2(sidex1 , sidey1)

    elif sidey1<0:
        if sidex1>0:
            new_angle1 = math.pi - math.atan2(sidex1, sidey1)
        else:
            new_angle1 = math.atan2(sidex1 , sidey1)

    elif sidey1==0:
        new_angle1 = math.pi / 2

    else:
        new_angle1 = math.pi -math.atan2(sidex1 , sidey1)

    new_len1 = math.sqrt(sidex1 ** 2 + sidey1 ** 2)

    return new_angle0, new_angle1, new_len0, new_len1
