# exec(open('place_and_route_rella.py').read())
import importlib

import pcbnew
from kadpy import kad, mat2, pnt, vec2

importlib.reload(kad)
importlib.reload(pnt)
importlib.reload(vec2)
importlib.reload(mat2)

kad.UnitMM = True
kad.PointDigits = 3

# alias
Strt = kad.Straight
Dird = kad.Directed
ZgZg = kad.ZigZag

Round = kad.Round
BezierRound = kad.BezierRound
LinearRound = kad.LinearRound

# in mm
VIA_Size = [(1.2, 0.6), (1.15, 0.5), (0.92, 0.4), (0.8, 0.3)]

via_size_pwr = VIA_Size[1]
via_size_dat = VIA_Size[2]
via_size_gnd = VIA_Size[3]

Cu_layers = ["F.Cu", "B.Cu", "In1.Cu", "In2.Cu"]

pcb = pcbnew.GetBoard()

GND = pcb.FindNet("GND")
VCC = pcb.FindNet("3V3")

board_width = 33
board_height = 2.54 * 7
board_size = (board_width, board_height)
board_orig = (100, 80)


def place_mods():
    kad.move_mods(
        board_orig,
        0,
        [
            ("J1", (0, 3.82), 0),
            ("C1", (9.4, -2.38), 0),
            ("C2", (2.4, -1.08), -90),
            (
                None,
                (12, 0),
                0,
                [
                    # ("U1", (-18.114, 1.296 + 2.54 * 3 - 0), 90),
                    ("J3", (0, +2.54 * 3), 90),
                    ("J4", (0, -2.54 * 3), 90),
                ],
            ),
            (
                None,
                (-10.4, -5.58),
                0,
                [
                    ("R4", (1.524 * 0, 0), -90),
                    ("R1", (1.524 * 1, 0), -90),
                    ("R2", (1.524 * 2, 0), -90),
                    ("R3", (1.524 * 3, 0), -90),
                ],
            ),
            (
                None,
                (-9.3, 3.82),
                0,
                [
                    ("R11", (-0.2175, -0.74), 0),
                    ("R12", (0.9125 * 2 + 0.2175, 0.74), 180),
                ],
            ),
        ],
    )


w_pwr, r_pwr = 0.60, 1.5  # power
w_led, r_led = 0.45, 1.2  # LED dat
w_dat, r_dat = 0.40, 0.7  # row / col

r_tri = 0.7


def wire_mod():
    rj45 = "J1"
    xiao_l = "J3"
    xiao_r = "J4"
    via_3v3_led = kad.add_via(kad.calc_pos_from_pad(rj45, "23", (0.6, -1.8)), VCC, via_size_pwr)
    # RJ45 - xiao_r
    via_5vd = kad.add_via_relative(rj45, "2", (0, -3.8), via_size_pwr)
    kad.wire_mod_pads(
        [
            # 5VD
            (xiao_r, "1", rj45, via_5vd, w_pwr, (Dird, 45, 90), "F.Cu"),
            # 5VD
            (rj45, "4", rj45, via_5vd, w_pwr, (Dird, [(+90, 1.5), 0], 90), "F.Cu"),
            (rj45, "16", rj45, via_5vd, w_pwr, (Dird, [(+90, 1.5), 0], 90, r_led), "F.Cu"),
            (rj45, "16", rj45, "4", w_pwr, (Dird, [(+90, 1.5), 0], 90, r_led), "F.Cu"),
            # GND
            # (xiao_r, "2", rj45, "2", w_pwr, (Dird, -45, 90), "In2.Cu"),
            # 3V3
            (xiao_r, "3", rj45, "6", w_pwr, (ZgZg, 0, 30), "In2.Cu"),
            # 3V3
            (rj45, "6", rj45, "18", w_pwr, (Dird, [(+90, 1.5), 0], 90, r_tri), "B.Cu"),
            (rj45, "18", rj45, via_3v3_led, w_pwr, (Dird, 90, -45, r_pwr), "F.Cu"),
            # LED1/2/3
            (xiao_r, "4", rj45, "9", w_led, (Dird, -45, [(-135, 2.0), (180, 1.7), (135, 2.0), 0], r_led), "In1.Cu"),
            (xiao_r, "5", rj45, "11", w_led, (Dird, -45, 90), "In1.Cu"),
            (xiao_r, "7", rj45, "21", w_led, (Dird, -45, 90), "In1.Cu"),
        ]
    )
    # RJ45 - xiao_l
    via_sda = kad.add_via_relative(rj45, "19", (2.0, 2.4), via_size_dat)
    via_sck = kad.add_via_relative(rj45, "15", (2.0, 2.4), via_size_dat)
    kad.wire_mod_pads(
        [
            # Full colr LED
            (xiao_l, "1", rj45, "1", w_dat, (Dird, [(0, 2), -45], 90), "In1.Cu"),
            (xiao_l, "2", rj45, "13", w_dat, (Dird, [(0, 3.2), 90], [(0, 5.6), -45], r_led), "In1.Cu"),
            # NRST
            (xiao_l, "3", rj45, "5", w_dat, (ZgZg, 0, 45), "F.Cu"),
            (xiao_l, "3", rj45, "17", w_dat, (Dird, [(0, 2.2), 90], 90, r_led), "In2.Cu"),
            # SCK
            (rj45, "3", rj45, "15", w_dat, (Dird, [(-90, 2.4), 0], 90, r_dat), "B.Cu"),
            (rj45, "3", xiao_l, "6", w_dat, (Dird, [(-90, 2.4), 0], 0, r_dat), "B.Cu"),
            (rj45, "15", xiao_l, "6", w_dat, (Dird, [(-90, 2.4), 0], 0, r_dat), "B.Cu"),
            (rj45, "3", "R12", "1", w_dat, (Dird, [(-90, 2.4), 0], 90, r_dat), "B.Cu"),
            (rj45, "15", "R12", "1", w_dat, (Strt), "B.Cu"),
            # SDA
            (rj45, "7", rj45, "19", w_dat, (Dird, [(-90, 2.4), 0], 90, r_dat), "F.Cu"),
            (rj45, "7", xiao_l, "5", w_dat, (Dird, [(-90, 2.4), 0], 0, r_dat), "F.Cu"),
            (rj45, "19", xiao_l, "5", w_dat, (Dird, [(-90, 2.4), 0], 0, r_dat), "F.Cu"),
            (rj45, "19", "R11", "1", w_dat, (Dird, 90, 0, r_dat), "B.Cu"),
        ]
    )
    # I2C 3V3
    via_left = kad.add_via_relative(rj45, "20", (-1.6, 0), via_size_pwr)
    kad.wire_mod_pads(
        [
            (rj45, "18", rj45, via_left, w_led, (Dird, [(90, 1.5), 0], 90, r_led), "B.Cu"),
            (rj45, via_left, "R12", "2", w_led, (Dird, [(-90, 0.4), (-60, 3.2), 90], 0, r_led), "B.Cu"),
            ("R11", "2", "R12", "2", w_led, (ZgZg, 90, 45), "B.Cu"),
        ]
    )
    # LED
    kad.wire_mod_pads(
        [
            # LED1/2/3
            (rj45, "24", "R4", "2", w_led, (Dird, 90, [(0, 1.6), 90], r_led), "B.Cu"),
            (rj45, "22", "R3", "2", w_led, (Dird, 90, [(0, 0.0), 90], r_led), "B.Cu"),
            (rj45, "12", "R2", "2", w_led, (Dird, 90, [(0, 1.0), 90], r_led), "B.Cu"),
            (rj45, "10", "R1", "2", w_led, (Dird, 0, [(0, 1.8), (-90, 10), (-135, 0.5 * 1.414), (-90, 3.2), -135], r_led), "B.Cu"),
            # LED4
            (rj45, "23", rj45, via_left, w_led, (ZgZg, 90, 30), "In1.Cu"),
            (xiao_l, "4", rj45, via_left, w_led, (Dird, [(0, 2.2), 90], [(-90, 0.4), -60], r_led), "In1.Cu"),
            # 3V3
            (rj45, via_3v3_led, "R4", "1", w_pwr, (Dird, -45, 90, r_tri), "B.Cu"),
            ("R4", "1", "R3", "1", w_pwr, (Strt), "B.Cu"),
            ("R3", "1", "R4", "1", w_pwr, (Strt), "B.Cu"),
        ]
    )
    # C1/2
    kad.wire_mod_pads(
        [
            ("C1", "2", rj45, "2", w_pwr, (Dird, 45, 90), "B.Cu"),
            ("C1", "1", rj45, "4", w_pwr, (Dird, 135, 90), "B.Cu"),
            ("C2", "2", rj45, "8", w_pwr, (Dird, 45, 0), "B.Cu"),
        ]
    )
    for via in [via_5vd, via_left, via_sda, via_sck]:
        pcb.Delete(via)

    # gnd vias
    for pad in "1234567":
        kad.add_via(kad.calc_pos_from_pad(xiao_l, pad, (1.2, -2.54 / 2)), GND, via_size_dat)
    for pad in ["1", "3", "5"]:
        kad.add_via(kad.calc_pos_from_pad(rj45, pad, (-2.02 / 2, 1.4)), GND, via_size_dat)
    for pad in ["15", "17"]:
        kad.add_via(kad.calc_pos_from_pad(rj45, pad, (+2.02 / 2, 1.4)), GND, via_size_dat)
    kad.add_via(kad.calc_pos_from_pad(rj45, "24", (+2.29 / 2, +1.2)), GND, via_size_dat)
    kad.add_via(kad.calc_pos_from_pad(rj45, "24", (+2.29 / 2, -1.2)), GND, via_size_dat)
    kad.add_via(kad.calc_pos_from_pad(rj45, "10", (+2.29 / 2, -1.2)), GND, via_size_dat)
    kad.add_via(kad.calc_pos_from_pad(rj45, "20", (-2.8, 0)), GND, via_size_dat)
    kad.add_via(kad.calc_pos_from_pad(rj45, "20", (0, 6.4)), GND, via_size_dat)
    kad.add_via(kad.calc_pos_from_pad(rj45, "11", (1.8, 0)), GND, via_size_dat)


def draw_edge_cuts():
    width = 0.12

    Radius = 0.64
    Oy = vec2.add(kad.get_mod_pos("J3"), kad.get_mod_pos("J4"))[1] / 2
    _org = (board_orig[0], Oy)
    cnrs = [
        ((vec2.add(_org, (0, -board_height / 2)), 0), Round, [Radius]),
        ((vec2.add(_org, (+board_width / 2, 0)), 90), Round, [Radius]),
        ((vec2.add(_org, (0, +board_height / 2)), 180), Round, [Radius]),
        ((vec2.add(_org, (-board_width / 2, 0)), 270), Round, [Radius]),
    ]
    kad.draw_closed_corners(cnrs, "Edge.Cuts", width)


# References
def set_text_prop(text, pos, angle, offset_length, offset_angle, text_angle):
    if text_angle == None:
        text.SetVisible(False)
    else:
        # tsz = 1.0
        tsz = 0.9
        text.SetTextSize(pcbnew.wxSizeMM(tsz, tsz))
        text.SetTextThickness(pcbnew.FromMM(0.18))
        pos_text = vec2.scale(offset_length, vec2.rotate(-(offset_angle + angle)), pos)
        text.SetPosition(pnt.to_unit(vec2.round(pos_text, 3), True))
        text.SetTextAngle(text_angle * 10)
        text.SetKeepUpright(False)


def set_refs():
    # hide value texts
    # for mod in pcb.GetFootprints():
    #     ref = mod.Reference()
    #     val = mod.Value()
    #     val.SetVisible(False)
    refs = [
        (3.2, 90, 0, ["J1"]),
        (2.4, 0, -90, ["R1", "R3"]),
        (2.4, 180, 90, ["R2", "R4"]),
        (1.8, -135, 180, ["R11"]),
        (3.2, 180, 0, ["R12"]),
        (1.6, 90, 0, ["C1"]),
        (1.6, -90, 180, ["C2"]),
    ]
    for offset_length, offset_angle, text_angle, mod_names in refs:
        for mod_name in mod_names:
            mod = kad.get_mod(mod_name)
            if mod is None:
                continue
            pos, angle = kad.get_mod_pos_angle(mod_name)
            ref = mod.Reference()
            set_text_prop(ref, pos, angle, offset_length, offset_angle, text_angle)
            for item in mod.GraphicalItems():
                if type(item) is pcbnew.FP_TEXT and item.GetShownText() == ref.GetShownText():
                    set_text_prop(item, pos, angle, offset_length, offset_angle, text_angle)
    tsz = 0.8

    # J1
    angle = kad.get_mod_angle("J1")
    # pads = ["RGB", "GND", "SCK", "5VD", "nRST", "3V3", "SDA", "GND"]
    pads = ["FC", "GD", "SC", "5V", "nR", "3V", "SD", "GD"]
    for idx, pad in enumerate(pads):
        _pad = pad
        # Right
        if pad == "FC":
            _pad = pad + "1"
        pos = kad.calc_pos_from_pad("J1", f"{idx+1}", (0, 1.6 * (1 if (idx + 1) % 2 == 1 else -1)))
        kad.add_text(pos, angle, _pad, "F.SilkS", (tsz, tsz), 0.15, pcbnew.GR_TEXT_HJUSTIFY_CENTER, pcbnew.GR_TEXT_VJUSTIFY_CENTER)
        if idx in [1]:
            pos = kad.calc_pos_from_pad("J1", "2", (2.0, 0))
        elif idx in [3]:
            pos = kad.calc_pos_from_pad("J1", "6", (0.5, -2.8))
        kad.add_text(pos, angle, _pad, "B.SilkS", (tsz, tsz), 0.15, pcbnew.GR_TEXT_HJUSTIFY_CENTER, pcbnew.GR_TEXT_VJUSTIFY_CENTER)
        # Left
        if pad == "FC":
            _pad = pad + "2"
        pos = kad.calc_pos_from_pad("J1", f"{idx+13}", (0, 1.6 * (1 if (idx + 1) % 2 == 1 else -1)))
        if idx in [4, 6]:
            pos = vec2.add(pos, (-4, -1.6))
        kad.add_text(pos, angle, _pad, "F.SilkS", (tsz, tsz), 0.15, pcbnew.GR_TEXT_HJUSTIFY_CENTER, pcbnew.GR_TEXT_VJUSTIFY_CENTER)
        kad.add_text(pos, angle, _pad, "B.SilkS", (tsz, tsz), 0.15, pcbnew.GR_TEXT_HJUSTIFY_CENTER, pcbnew.GR_TEXT_VJUSTIFY_CENTER)

    # J1
    angle = kad.get_mod_angle("J1") - 180
    pads = [(9, "D1"), (11, "D2"), (21, "D3"), (23, "D4")]
    for idx, (pin, pad) in enumerate(pads):
        pos = kad.calc_pos_from_pad("J1", f"{pin}", (0, 1.6))
        kad.add_text(pos, angle, pad, "F.SilkS", (tsz, tsz), 0.15, pcbnew.GR_TEXT_HJUSTIFY_CENTER, pcbnew.GR_TEXT_VJUSTIFY_CENTER)
        kad.add_text(pos, angle, pad, "B.SilkS", (tsz, tsz), 0.15, pcbnew.GR_TEXT_HJUSTIFY_CENTER, pcbnew.GR_TEXT_VJUSTIFY_CENTER)

    # J3
    angle = kad.get_mod_angle("J3") - 90
    pads = ["FC1", "FC2", "nR", "D4", "SD", "SC", "x"]
    for idx, pad in enumerate(pads):
        pos = kad.calc_pos_from_pad("J3", f"{idx+1}", (1.6, 0))
        kad.add_text(pos, angle, pad, "F.SilkS", (tsz, tsz), 0.15, pcbnew.GR_TEXT_HJUSTIFY_CENTER, pcbnew.GR_TEXT_VJUSTIFY_CENTER)
        kad.add_text(pos, angle, pad, "B.SilkS", (tsz, tsz), 0.15, pcbnew.GR_TEXT_HJUSTIFY_CENTER, pcbnew.GR_TEXT_VJUSTIFY_CENTER)

    # J4
    angle = kad.get_mod_angle("J4") + 90
    pads = ["5V", "GD", "3V", "D1", "D2", "x", "D3"]
    for idx, pad in enumerate(pads):
        pos = kad.calc_pos_from_pad("J4", f"{idx+1}", (-1.1, -1.27))
        kad.add_text(pos, angle, pad, "F.SilkS", (tsz, tsz), 0.15, pcbnew.GR_TEXT_HJUSTIFY_CENTER, pcbnew.GR_TEXT_VJUSTIFY_CENTER)
        kad.add_text(pos, angle, pad, "B.SilkS", (tsz, tsz), 0.15, pcbnew.GR_TEXT_HJUSTIFY_CENTER, pcbnew.GR_TEXT_VJUSTIFY_CENTER)


def add_zone(net_name, layer_name, rect):
    settings = pcb.GetZoneSettings()
    settings.m_ZoneClearance = pcbnew.FromMils(12)
    pcb.SetZoneSettings(settings)

    zone = kad.add_zone(rect, layer_name, net_name)
    zone.SetMinThickness(pcbnew.FromMils(13))
    zone.SetThermalReliefGap(pcbnew.FromMils(13))
    # zone.Hatch()


def main():
    place_mods()
    wire_mod()
    draw_edge_cuts()
    set_refs()

    # logo
    for mod, angle in [("G1", 180)]:
        if kad.get_mod(mod) is not None:
            kad.move_mods((90, 87), 0, [(mod, (0, 0), angle)])

    # zones
    rect = kad.make_rect(vec2.scale(1.1, board_size), vec2.scale(-0.5 * 1.1, board_size, board_orig))
    for layer in Cu_layers:
        add_zone("GND", layer, rect)

    # name
    kad.add_text((105, 84.4), 0, f"orihikarna 24/10/05", "B.Silkscreen", (0.8, 0.8), 0.4, pcbnew.GR_TEXT_HJUSTIFY_CENTER, pcbnew.GR_TEXT_VJUSTIFY_CENTER)


if __name__ == "__main__":
    kad.removeDrawings()
    kad.removeTracksAndVias()
    main()
    pcbnew.Refresh()
