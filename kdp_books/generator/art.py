"""Vector line-art library (original, code-generated). Every subject is drawn in a
+-100 unit box, centred on (cx, cy), scaled so that 100 units == s points."""
import math, random
from reportlab.lib.colors import black, white

_LW = [1.0]


def begin(c, cx, cy, s, lw=3.2):
    c.saveState()
    c.translate(cx, cy)
    k = s / 100.0
    c.scale(k, k)
    _LW[0] = lw / k
    c.setLineWidth(_LW[0])
    c.setLineJoin(1)
    c.setLineCap(1)
    c.setStrokeColor(black)
    c.setFillColor(white)
    return k


def end(c):
    c.restoreState()


def _shape(c, sh, black_pass):
    lw = _LW[0]
    t = sh[0]
    if t == 'l':
        _, x1, y1, x2, y2, w = sh
        c.setLineWidth(w + 2 * lw if black_pass else w)
        c.line(x1, y1, x2, y2)
        return
    if t == 'pl':
        _, pts, w = sh
        c.setLineWidth(w + 2 * lw if black_pass else w)
        p = c.beginPath()
        p.moveTo(*pts[0])
        for q in pts[1:]:
            p.lineTo(*q)
        c.drawPath(p, stroke=1, fill=0)
        return
    c.setLineWidth(2 * lw)
    st = 1 if black_pass else 0
    if t == 'c':
        c.circle(sh[1], sh[2], sh[3], stroke=st, fill=1)
    elif t == 'e':
        c.ellipse(sh[1], sh[2], sh[3], sh[4], stroke=st, fill=1)
    elif t == 'r':
        c.roundRect(sh[1], sh[2], sh[3], sh[4], sh[5], stroke=st, fill=1)
    elif t == 'p':
        p = c.beginPath()
        p.moveTo(*sh[1][0])
        for q in sh[1][1:]:
            p.lineTo(*q)
        p.close()
        c.drawPath(p, stroke=st, fill=1)


def union(c, shapes):
    """Draw the outer outline of the union of shapes (white inside)."""
    c.setFillColor(black)
    c.setStrokeColor(black)
    for sh in shapes:
        _shape(c, sh, True)
    c.setFillColor(white)
    c.setStrokeColor(white)
    for sh in shapes:
        _shape(c, sh, False)
    c.setStrokeColor(black)
    c.setLineWidth(_LW[0])


def ink(c):
    c.setStrokeColor(black)
    c.setFillColor(white)
    c.setLineWidth(_LW[0])


def dot(c, x, y, r):
    c.setFillColor(black)
    c.circle(x, y, r, stroke=0, fill=1)
    c.setFillColor(white)


def poly(c, pts, fill=1, stroke=1, close=True):
    p = c.beginPath()
    p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    if close:
        p.close()
    c.drawPath(p, stroke=stroke, fill=fill)


def curve(c, pts):
    poly(c, pts, fill=0, stroke=1, close=False)


def star_pts(cx, cy, R, r, n=5, rot=90):
    out = []
    for i in range(2 * n):
        a = math.radians(rot + i * 180.0 / n)
        rad = R if i % 2 == 0 else r
        out.append((cx + rad * math.cos(a), cy + rad * math.sin(a)))
    return out


# ------------------------------------------------------------------ subjects
def tree(c, cx, cy, s, lw=3.2):
    begin(c, cx, cy, s, lw)
    union(c, [('p', [(-85, -40), (85, -40), (0, 25)]),
              ('p', [(-68, -2), (68, -2), (0, 58)]),
              ('p', [(-50, 38), (50, 38), (0, 92)]),
              ('r', -14, -88, 28, 50, 0)])
    for x, y, r in [(-42, -28, 8), (36, -26, 8), (0, -22, 6), (-26, 14, 7), (28, 16, 7), (0, 58, 6), (-5, 30, 5)]:
        c.circle(x, y, r, stroke=1, fill=1)
    curve(c, [(-62, -4), (-30, -12), (0, -8), (30, -12), (62, -4)])
    curve(c, [(-40, 36), (-15, 30), (15, 34), (40, 36)])
    poly(c, star_pts(0, 100, 15, 6.5))
    end(c)


def snowman(c, cx, cy, s, lw=3.2):
    begin(c, cx, cy, s, lw)
    union(c, [('c', 0, -62, 38), ('c', 0, -8, 31), ('c', 0, 38, 22)])
    # arms
    c.setLineWidth(_LW[0] * 1.6)
    for sx in (-1, 1):
        c.line(sx * 30, -2, sx * 74, 24)
        c.line(sx * 56, 14, sx * 64, 32)
        c.line(sx * 62, 18, sx * 78, 12)
    ink(c)
    # hat
    c.roundRect(-16, 64, 32, 34, 3, stroke=1, fill=1)
    c.roundRect(-30, 57, 60, 9, 3, stroke=1, fill=1)
    c.line(-16, 72, 16, 72)
    # face
    dot(c, -8, 43, 2.6); dot(c, 8, 43, 2.6)
    poly(c, [(0, 37), (22, 32), (0, 31)])
    for x, y in [(-10, 29), (-5, 26), (5, 26), (10, 29)]:
        dot(c, x, y, 1.8)
    # scarf
    c.roundRect(-24, 14, 48, 9, 3, stroke=1, fill=1)
    c.roundRect(6, -14, 13, 30, 3, stroke=1, fill=1)
    for y in (-4, -10): c.line(6, y, 19, y)
    for y in (6, -8, -24): c.circle(0, y - 8, 3.6, stroke=1, fill=1)
    for y in (-50, -66): c.circle(0, y, 3.6, stroke=1, fill=1)
    # snow
    for x, y in [(-60, -95), (60, -90), (-72, 70), (75, 70)]:
        c.circle(x, y, 3, stroke=1, fill=1)
    end(c)


def gift(c, cx, cy, s, lw=3.2):
    begin(c, cx, cy, s, lw)
    union(c, [('r', -62, -75, 124, 100, 3), ('r', -70, 20, 140, 32, 4), ('e', -52, 48, -4, 90), ('e', 4, 48, 52, 90)])
    c.roundRect(-14, -75, 28, 127, 0, stroke=1, fill=1)
    c.ellipse(-52, 48, -4, 90, stroke=1, fill=1)
    c.ellipse(4, 48, 52, 90, stroke=1, fill=1)
    c.circle(0, 52, 11, stroke=1, fill=1)
    for sx in (-1, 1):
        c.line(sx * 8, 62, sx * 32, 80)
        c.line(sx * 14, 52, sx * 40, 64)
    for x, y in [(-40, -30), (-30, -55), (38, -20), (42, -50), (-45, 0)]:
        poly(c, star_pts(x, y, 7, 3), fill=1)
    end(c)


def star(c, cx, cy, s, lw=3.2):
    begin(c, cx, cy, s, lw)
    pts = star_pts(0, -4, 98, 42)
    union(c, [('p', pts)])
    for p in pts[1::2]:
        c.line(0, -4, p[0], p[1])
    for p in pts[0::2]:
        c.line(0, -4, p[0] * 0.55, p[1] * 0.55 - 2)
    end(c)


def candycane(c, cx, cy, s, lw=3.2):
    begin(c, cx, cy, s, lw)
    pts = [(38, -92), (38, 25)]
    for i in range(1, 25):
        a = math.radians(i * 180.0 / 24)
        pts.append((38 * math.cos(a) * 1.0 + 0, 25 + 38 * math.sin(a)))
    pts.append((-38, 5))
    union(c, [('pl', pts, 34)])
    # stripes: perpendicular slashes along centre line
    seg = []
    for i in range(len(pts) - 1):
        seg.append((pts[i], pts[i + 1]))
    c.setLineWidth(_LW[0])
    acc = 0.0
    step = 20.0
    nxt = 8.0
    for (a, b) in seg:
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        while nxt <= acc + L:
            t = (nxt - acc) / L
            px, py = a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t
            dx, dy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
            nx, ny = -dy, dx
            ang = math.radians(35)
            ux = nx * math.cos(ang) - dx * math.sin(ang)
            uy = ny * math.cos(ang) - dy * math.sin(ang)
            c.line(px - ux * 17, py - uy * 17, px + ux * 17, py + uy * 17)
            nxt += step
        acc += L
    # bow
    ink(c)
    c.ellipse(-52, -30, -20, -10, stroke=1, fill=1)
    c.ellipse(-26, -30, 6, -10, stroke=1, fill=1)
    c.circle(-23, -20, 6, stroke=1, fill=1)
    end(c)


def gingerbread(c, cx, cy, s, lw=3.2):
    begin(c, cx, cy, s, lw)
    union(c, [('c', 0, 62, 30), ('r', -30, -28, 60, 80, 14),
              ('l', -24, 38, -72, 12, 26), ('l', 24, 38, 72, 12, 26),
              ('l', -15, -26, -30, -80, 28), ('l', 15, -26, 30, -80, 28)])
    dot(c, -10, 68, 3); dot(c, 10, 68, 3)
    curve(c, [(-12, 54), (-6, 49), (0, 48), (6, 49), (12, 54)])
    for y in (28, 8, -12):
        c.circle(0, y, 5, stroke=1, fill=1)
    # icing
    for sx in (-1, 1):
        curve(c, [(sx * 58, 22), (sx * 60, 14), (sx * 64, 22), (sx * 66, 12)])
        curve(c, [(sx * 20, -68), (sx * 28, -62), (sx * 34, -70), (sx * 40, -64)])
    curve(c, [(-28, 40), (-14, 34), (0, 40), (14, 34), (28, 40)])
    end(c)


def mitten(c, cx, cy, s, lw=3.2):
    begin(c, cx, cy, s, lw)
    union(c, [('r', -48, -42, 96, 126, 42), ('e', -92, -6, -36, 52), ('r', -54, -92, 108, 52, 10)])
    # cuff pattern
    c.roundRect(-54, -92, 108, 52, 10, stroke=1, fill=0)
    for y in (-60, -72):
        pts = []
        x = -54
        up = True
        while x <= 54:
            pts.append((x, y + (5 if up else -5)))
            up = not up
            x += 9
        curve(c, pts)
    # snowflake motif
    for i in range(6):
        a = math.radians(i * 60)
        c.line(4, 28, 4 + 26 * math.cos(a), 28 + 26 * math.sin(a))
        bx, by = 4 + 16 * math.cos(a), 28 + 16 * math.sin(a)
        for d in (-40, 40):
            b = a + math.radians(d)
            c.line(bx, by, bx + 8 * math.cos(b), by + 8 * math.sin(b))
    end(c)


def ornament(c, cx, cy, s, lw=3.2, v=0):
    begin(c, cx, cy, s, lw)
    union(c, [('c', 0, -12, 66), ('r', -18, 50, 36, 22, 4)])
    c.circle(0, 82, 10, stroke=1, fill=0)
    c.line(-18, 60, 18, 60)
    c.saveState()
    p = c.beginPath()
    p.circle(0, -12, 62)
    c.clipPath(p, stroke=0, fill=0)
    v = v % 6
    if v == 0:
        for y in range(-60, 50, 22):
            curve(c, [(-70 + i * 10, y + (6 if (i % 2) else -6)) for i in range(15)])
    elif v == 1:
        for t in range(-120, 121, 34):
            c.line(t - 100, -112, t + 100, 88)
            c.line(t + 100, -112, t - 100, 88)
    elif v == 2:
        for gx in range(-60, 61, 26):
            for gy in range(-66, 50, 26):
                c.circle(gx + (13 if ((gy // 26) % 2) else 0), gy, 6, stroke=1, fill=1)
    elif v == 3:
        for y in (-52, -26, 0, 26):
            curve(c, [(-70 + i * 14, y + (9 if (i % 2) else -9)) for i in range(11)])
    elif v == 4:
        for r in (48, 33):
            c.circle(0, -12, r, stroke=1, fill=0)
        poly(c, star_pts(0, -12, 20, 8), fill=1)
    else:
        for w in (18, 38, 58):
            c.ellipse(-w, -80, w, 56, stroke=1, fill=0)
    c.restoreState()
    end(c)


def wreath(c, cx, cy, s, lw=3.0):
    begin(c, cx, cy, s, lw)
    for layer, R, off in ((0, 68, 0), (1, 54, 12)):
        n = 14
        for i in range(n):
            a = math.radians(i * 360.0 / n + off)
            c.saveState()
            c.translate(R * math.cos(a), R * math.sin(a) + 4)
            c.rotate(math.degrees(a) + 90 + (35 if layer == 0 else -35))
            c.ellipse(-9, -22, 9, 22, stroke=1, fill=1)
            c.line(0, -18, 0, 16)
            c.restoreState()
    for ang in (30, 100, 160, 230, 290, 350):
        a = math.radians(ang)
        c.circle(63 * math.cos(a), 63 * math.sin(a) + 4, 6, stroke=1, fill=1)
    # bow
    c.saveState(); c.translate(0, -62); c.rotate(32)
    c.ellipse(-44, -9, -2, 15, stroke=1, fill=1); c.restoreState()
    c.saveState(); c.translate(0, -62); c.rotate(-32)
    c.ellipse(2, -9, 44, 15, stroke=1, fill=1); c.restoreState()
    poly(c, [(-6, -66), (-24, -96), (-8, -90), (-2, -70)])
    poly(c, [(6, -66), (24, -96), (8, -90), (2, -70)])
    c.circle(0, -62, 9, stroke=1, fill=1)
    end(c)


def penguin(c, cx, cy, s, lw=3.2):
    begin(c, cx, cy, s, lw)
    union(c, [('e', -50, -84, 50, 46), ('e', -36, 14, 36, 80),
              ('l', -46, 14, -74, -34, 16), ('l', 46, 14, 74, -34, 16),
              ('e', -42, -96, -4, -78), ('e', 4, -96, 42, -78)])
    c.ellipse(-32, -76, 32, 22, stroke=1, fill=0)
    dot(c, -13, 52, 3.5); dot(c, 13, 52, 3.5)
    poly(c, [(-10, 40), (10, 40), (0, 28)])
    # scarf
    c.roundRect(-30, 8, 60, 12, 4, stroke=1, fill=1)
    c.roundRect(10, -22, 14, 36, 3, stroke=1, fill=1)
    # hat
    poly(c, [(-34, 72), (34, 72), (8, 112), (-4, 100)])
    c.roundRect(-38, 66, 76, 12, 5, stroke=1, fill=1)
    c.circle(10, 112, 8, stroke=1, fill=1)
    end(c)


def santahat(c, cx, cy, s, lw=3.2):
    begin(c, cx, cy, s, lw)
    union(c, [('p', [(-62, -40), (62, -40), (44, 20), (16, 62), (-28, 78), (-50, 40)]),
              ('r', -74, -72, 148, 38, 17), ('c', -34, 84, 17)])
    c.roundRect(-74, -72, 148, 38, 17, stroke=1, fill=1)
    c.circle(-34, 84, 17, stroke=1, fill=1)
    for x, y in [(-48, -53), (-20, -50), (10, -54), (38, -50), (58, -56)]:
        c.circle(x, y, 3, stroke=1, fill=0)
    curve(c, [(-40, -10), (-5, 10), (28, 0)])
    curve(c, [(-34, 34), (0, 38), (24, 32)])
    end(c)


def stocking(c, cx, cy, s, lw=3.2):
    begin(c, cx, cy, s, lw)
    union(c, [('r', -36, -30, 72, 120, 8), ('r', -36, -78, 108, 56, 28), ('r', -44, 62, 88, 32, 8)])
    c.roundRect(-44, 62, 88, 32, 8, stroke=1, fill=1)
    for x in (-24, 0, 24):
        c.line(x - 6, 62, x + 6, 94)
    for y in (24, 4, -16):
        c.line(-36, y, 36, y)
    c.circle(8, -56, 6, stroke=1, fill=0)
    c.circle(0, 100, 5, stroke=1, fill=0)
    end(c)


def bell(c, cx, cy, s, lw=3.2):
    begin(c, cx, cy, s, lw)
    pts = [(-70, -42), (-52, -30)]
    for i in range(0, 31):
        a = math.radians(180 - i * 6)
        pts.append((46 * math.cos(a), 24 + 52 * math.sin(a)))
    pts += [(52, -30), (70, -42)]
    union(c, [('p', pts), ('c', 0, -52, 13)])
    c.line(-61, -36, 61, -36)
    c.circle(0, -58, 14, stroke=1, fill=1)
    c.ellipse(-26, 52, 26, 70, stroke=1, fill=1)
    # holly
    for sx in (-1, 1):
        c.saveState(); c.translate(sx * 20, 66); c.rotate(sx * -30)
        c.ellipse(-4, -14, 4, 14, stroke=1, fill=1)
        c.restoreState()
    c.circle(0, 62, 5, stroke=1, fill=1)
    for x, y in [(-22, 30), (6, 40), (24, 20), (-8, 10)]:
        poly(c, star_pts(x, y, 6, 2.6), fill=1)
    end(c)


def cabin(c, cx, cy, s, lw=3.2):
    begin(c, cx, cy, s, lw)
    union(c, [('r', -70, -80, 140, 80, 0), ('p', [(-86, 0), (86, 0), (0, 70)]), ('r', 36, 30, 22, 50, 0)])
    c.roundRect(-18, -80, 36, 56, 3, stroke=1, fill=1)
    c.circle(10, -52, 2.5, stroke=1, fill=1)
    for sx in (-1, 1):
        c.roundRect(sx * 42 - 14, -48, 28, 28, 2, stroke=1, fill=1)
        c.line(sx * 42, -48, sx * 42, -20); c.line(sx * 42 - 14, -34, sx * 42 + 14, -34)
    c.circle(0, 22, 12, stroke=1, fill=1)
    c.line(-72, -62, 72, -62)
    # smoke + snow
    curve(c, [(47, 84), (40, 94), (50, 102), (44, 112)])
    for x, y in [(-70, 60), (-50, 80), (60, 56), (74, 74), (-20, 96)]:
        c.circle(x, y, 3, stroke=1, fill=1)
    end(c)


def mug(c, cx, cy, s, lw=3.2):
    begin(c, cx, cy, s, lw)
    union(c, [('r', -54, -64, 100, 100, 16), ('c', 52, -12, 28)])
    c.circle(52, -12, 14, stroke=1, fill=1)
    c.roundRect(-54, -64, 100, 100, 16, stroke=1, fill=1)
    c.roundRect(-56, 28, 104, 14, 6, stroke=1, fill=1)
    for x in (-34, -6, 22):
        c.roundRect(x, 42, 24, 18, 6, stroke=1, fill=1)
    for x in (-36, -8, 20):
        curve(c, [(x + 6, 72), (x - 2, 84), (x + 10, 94), (x + 2, 106)])
    poly(c, star_pts(-4, -20, 22, 9), fill=1)
    c.line(-54, -40, 46, -40)
    end(c)


def reindeer(c, cx, cy, s, lw=3.2):
    begin(c, cx, cy, s, lw)
    c.setLineWidth(_LW[0] * 1.3)
    for sx in (-1, 1):
        c.line(sx * 28, 38, sx * 44, 82); c.line(sx * 44, 82, sx * 40, 100)
        c.line(sx * 36, 62, sx * 62, 74); c.line(sx * 62, 74, sx * 70, 92)
        c.line(sx * 42, 80, sx * 20, 92)
    ink(c)
    union(c, [('e', -88, 16, -40, 50), ('e', 40, 16, 88, 50),
              ('p', [(-48, 50), (48, 50), (36, -58), (0, -80), (-36, -58)])])
    dot(c, -18, 14, 4); dot(c, 18, 14, 4)
    c.circle(0, -62, 16, stroke=1, fill=1)
    curve(c, [(-10, -36), (0, -42), (10, -36)])
    poly(c, star_pts(0, 60, 0.1, 0.1), fill=0, stroke=0)
    for x, y in [(-20, 38), (0, 42), (20, 38)]:
        c.circle(x, y, 2, stroke=1, fill=1)
    end(c)


def snowflake(c, cx, cy, s, lw=2.6, seed=0):
    rng = random.Random(seed)
    begin(c, cx, cy, s, lw)
    nb = rng.randint(2, 4)
    br = sorted(rng.uniform(0.28, 0.82) for _ in range(nb))
    bl = [rng.uniform(0.18, 0.34) for _ in range(nb)]
    ba = [math.radians(rng.choice([40, 50, 60])) for _ in range(nb)]
    kind = rng.randint(0, 2)
    R = 96
    for i in range(6):
        c.saveState()
        c.rotate(60 * i)
        c.line(0, 0, R, 0)
        for t, l, a in zip(br, bl, ba):
            x = R * t
            L = R * l
            for sg in (-1, 1):
                c.line(x, 0, x + L * math.cos(a), sg * L * math.sin(a))
        ex = R
        if kind == 0:
            poly(c, [(ex, 0), (ex - 10, 7), (ex - 24, 0), (ex - 10, -7)])
        elif kind == 1:
            c.circle(ex - 5, 0, 5, stroke=1, fill=1)
        else:
            c.line(ex, 0, ex + 0, 0)
            for sg in (-1, 1):
                c.line(ex - 12, 0, ex + 2, sg * 9)
        c.restoreState()
    for rr in (R * (br[0] - 0.08), R * (br[-1] - 0.04)):
        pts = [(rr * math.cos(math.radians(60 * i)), rr * math.sin(math.radians(60 * i))) for i in range(6)]
        poly(c, pts, fill=0)
    end(c)


def mandala(c, cx, cy, s, lw=2.2, seed=0):
    rng = random.Random(seed * 7 + 3)
    n = rng.choice([8, 10, 12, 16])
    begin(c, cx, cy, s, lw)
    r = 8.0
    c.circle(0, 0, r, stroke=1, fill=0)
    layers = rng.randint(5, 7)
    gap = 88.0 / layers
    for L in range(layers):
        r0 = 8 + L * gap
        r1 = r0 + gap
        kind = rng.choice(['petal', 'ring', 'dots', 'tri', 'scallop'])
        for i in range(n):
            a = 2 * math.pi * i / n + (math.pi / n if L % 2 else 0)
            ca, sa = math.cos(a), math.sin(a)
            w = (math.pi / n) * r0 * 0.9
            if kind == 'petal':
                c.saveState(); c.rotate(math.degrees(a))
                p = c.beginPath(); p.moveTo(r0, 0)
                p.curveTo(r0 + gap * 0.3, w, r1 - gap * 0.2, w * 1.0, r1, 0)
                p.curveTo(r1 - gap * 0.2, -w * 1.0, r0 + gap * 0.3, -w, r0, 0)
                c.drawPath(p, stroke=1, fill=0)
                c.circle(r0 + gap * 0.5, 0, gap * 0.14, stroke=1, fill=0)
                c.restoreState()
            elif kind == 'dots':
                c.circle((r0 + r1) / 2 * ca, (r0 + r1) / 2 * sa, gap * 0.28, stroke=1, fill=0)
            elif kind == 'tri':
                w2 = (math.pi / n) * r1 * 0.8
                pts = [(r0 * math.cos(a - w2 / r0), r0 * math.sin(a - w2 / r0)),
                       (r0 * math.cos(a + w2 / r0), r0 * math.sin(a + w2 / r0)),
                       (r1 * ca, r1 * sa)]
                poly(c, pts, fill=0)
            elif kind == 'scallop':
                c.saveState(); c.rotate(math.degrees(a))
                c.arc(r0 - gap * 0.5 + 0.0, -gap * 0.5, r0 + gap * 0.5 + gap * 0.5, gap * 0.5, -90, 180)
                c.restoreState()
        c.circle(0, 0, r1, stroke=1, fill=0)
    end(c)


SUBJECTS = {
    'tree': tree, 'snowman': snowman, 'gift': gift, 'star': star, 'candy cane': candycane,
    'gingerbread man': gingerbread, 'mitten': mitten, 'wreath': wreath, 'penguin': penguin,
    'santa hat': santahat, 'stocking': stocking, 'bell': bell, 'cozy cabin': cabin,
    'hot cocoa': mug, 'reindeer': reindeer,
}


def orn(v):
    def f(c, cx, cy, s, lw=3.2):
        ornament(c, cx, cy, s, lw, v)
    return f


for _i in range(6):
    SUBJECTS['ornament %d' % (_i + 1)] = orn(_i)
