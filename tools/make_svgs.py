"""Erzeugt schematische Zeichnungen (SVG) für die Bildfragen.
Eigene Darstellungen – keine Abbildungen Dritter, daher frei verwendbar."""
import math, os, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "img"
os.makedirs(OUT, exist_ok=True)

INK = "#1d1d1b"
BLUE = "#009ee3"
ELEM = "#bfe5f7"

DEFS = f"""<defs>
<pattern id="h" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
<rect width="7" height="7" fill="#fff"/><line x1="0" y1="0" x2="0" y2="7" stroke="{INK}" stroke-width="1"/></pattern>
<pattern id="h2" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(-45)">
<rect width="7" height="7" fill="#fff"/><line x1="0" y1="0" x2="0" y2="7" stroke="{INK}" stroke-width="1"/></pattern>
</defs>"""


def svg(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">'
            f'{DEFS}<rect width="{w}" height="{h}" fill="#fff"/>{body}</svg>')


def save(name, w, h, body):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(svg(w, h, body))


RING = f'fill="url(#h)" stroke="{INK}" stroke-width="2" stroke-linejoin="round"'
RING2 = f'fill="url(#h2)" stroke="{INK}" stroke-width="2" stroke-linejoin="round"'
EL = f'fill="{ELEM}" stroke="{INK}" stroke-width="2"'
AX = f'stroke="{INK}" stroke-width="1.2" stroke-dasharray="14 4 3 4"'


def bearing(name, upper, W=320, H=280, cy=140):
    """upper = SVG der oberen Schnitthälfte; untere Hälfte wird gespiegelt."""
    body = (upper
            + f'<g transform="translate(0,{2*cy}) scale(1,-1)">{upper}</g>'
            + f'<line x1="20" y1="{cy}" x2="{W-20}" y2="{cy}" {AX}/>')
    save(name, W, H, body)


# 1 Rillenkugellager / deep groove ball bearing
r = 19
up = (f'<path d="M100,30 H220 V62 H176 A20,20 0 0 0 144,62 H100 Z" {RING}/>'
      f'<path d="M100,120 H220 V94 H176 A20,20 0 0 1 144,94 H100 Z" {RING2}/>'
      f'<circle cx="160" cy="78" r="{r}" {EL}/>')
bearing("lager_rillenkugellager.svg", up)

# 2 Schrägkugellager / angular contact ball bearing
up = (f'<path d="M100,30 H220 V56 H178 A20,20 0 0 0 141,66 H100 Z" {RING}/>'
      f'<path d="M100,120 H220 V92 H179 A20,20 0 0 1 142,100 H100 Z" {RING2}/>'
      f'<circle cx="160" cy="78" r="{r}" {EL}/>'
      f'<line x1="{160-40*math.sin(math.radians(35))}" y1="{78-40*math.cos(math.radians(35))}" '
      f'x2="{160+40*math.sin(math.radians(35))}" y2="{78+40*math.cos(math.radians(35))}" '
      f'stroke="{BLUE}" stroke-width="2" stroke-dasharray="5 3"/>')
bearing("lager_schraegkugellager.svg", up)

# 3 Pendelkugellager / self-aligning ball bearing (Außenring hohlkugelig)
R = 80; cx0, cy0 = 160, 140
def arc_y(x, R=R):
    return cy0 - math.sqrt(R*R - (x-cx0)**2)
x1, x2 = 122, 198
up = (f'<path d="M{x1},30 H{x2} V{arc_y(x2):.1f} A{R},{R} 0 0 0 {x1},{arc_y(x1):.1f} Z" {RING}/>'
      f'<path d="M{x1},118 H{x2} V96 H178 A15,15 0 0 1 160,93 A15,15 0 0 1 142,96 H{x1} Z" {RING2}/>')
for bx in (144, 176):
    by = cy0 - math.sqrt((R-14)**2 - (bx-cx0)**2)
    up += f'<circle cx="{bx}" cy="{by:.1f}" r="14" {EL}/>'
up += f'<path d="M95,{arc_y(95, R):.1f} A{R},{R} 0 0 1 225,{arc_y(225, R):.1f}" fill="none" stroke="{BLUE}" stroke-width="1.5" stroke-dasharray="5 3"/>'
bearing("lager_pendelkugellager.svg", up)

# 4 Zylinderrollenlager NU / cylindrical roller bearing
up = (f'<path d="M100,30 H220 V74 H206 V60 H114 V74 H100 Z" {RING}/>'
      f'<path d="M100,118 H220 V96 H100 Z" {RING2}/>'
      f'<rect x="118" y="61" width="84" height="34" rx="3" {EL}/>')
bearing("lager_zylinderrollenlager.svg", up)

# 5 Kegelrollenlager / tapered roller bearing
up = (f'<path d="M108,30 H220 V30 L220,64 L120,52 L108,52 Z" {RING}/>'
      f'<path d="M100,118 H220 V92 L208,92 L130,100 L114,101 L114,74 L100,74 Z" {RING2}/>'
      f'<path d="M117,55 L203,66 L205,90 L117,99 Z" {EL}/>')
bearing("lager_kegelrollenlager.svg", up)

# 6 Nadellager / needle roller bearing (sehr flach)
up = (f'<path d="M80,64 H240 V84 H232 V76 H88 V84 H80 Z" {RING}/>'
      f'<path d="M80,104 H240 V93 H80 Z" {RING2}/>'
      f'<rect x="92" y="77" width="136" height="15" rx="3" {EL}/>')
bearing("lager_nadellager.svg", up)

# 7 Pendelrollenlager / spherical roller bearing
x1, x2 = 118, 202
up = (f'<path d="M{x1},30 H{x2} V{arc_y(x2):.1f} A{R},{R} 0 0 0 {x1},{arc_y(x1):.1f} Z" {RING}/>'
      f'<path d="M{x1},118 H{x2} V96 L180,94 L166,90 L166,84 L154,84 L154,90 L140,94 L{x1},96 Z" {RING2}/>'
      f'<ellipse cx="139" cy="78" rx="19" ry="12" transform="rotate(-18 139 78)" {EL}/>'
      f'<ellipse cx="181" cy="78" rx="19" ry="12" transform="rotate(18 181 78)" {EL}/>')
bearing("lager_pendelrollenlager.svg", up)

# 8 Axial-Rillenkugellager / thrust ball bearing
up = (f'<path d="M118,118 V58 H136 V68 A19,19 0 0 0 136,92 V118 Z" {RING2}/>'
      f'<path d="M202,98 V38 H184 V68 A19,19 0 0 1 184,92 V98 Z" {RING}/>'
      f'<circle cx="160" cy="80" r="18" {EL}/>'
      f'<rect x="60" y="118" width="200" height="0.1" fill="none"/>')
bearing("lager_axialrillenkugellager.svg", up)


# ---------- Zahnräder ----------
def toothed(cx, cy, r_root, r_tip, z, rot=0.0, internal=False):
    """Umriss eines Zahnrads mit trapezförmigen Zähnen."""
    pts = []
    for i in range(z):
        a0 = rot + 2*math.pi*i/z
        da = 2*math.pi/z
        seq = [(a0, r_root), (a0+0.18*da, r_root), (a0+0.32*da, r_tip),
               (a0+0.58*da, r_tip), (a0+0.72*da, r_root)]
        for a, rr in seq:
            pts.append((cx + rr*math.cos(a), cy + rr*math.sin(a)))
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"


GEAR = f'fill="#ebf7fd" stroke="{INK}" stroke-width="2" stroke-linejoin="round"'
GEAR2 = f'fill="#bfe5f7" stroke="{INK}" stroke-width="2" stroke-linejoin="round"'


def flank_pair(name, kind):
    """Zwei Stirnräder in Seitenansicht (achsparallel) mit Flankenlinien."""
    W, H = 340, 260
    b = ""
    for (y0, h, mirror, fill) in ((30, 95, 1, "#ebf7fd"), (135, 95, -1, "#bfe5f7")):
        x0, w = 70, 200
        b += f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="{fill}" stroke="{INK}" stroke-width="2"/>'
        n = 12
        for i in range(-3, n+4):
            x = x0 + i*w/n
            if kind == "straight":
                segs = [((x, y0), (x, y0+h))]
            elif kind == "helical":
                s = 28*mirror
                segs = [((x, y0), (x+s, y0+h))]
            else:
                s = 22*mirror
                gap = 14 if kind == "double" else 0
                ym = y0 + h/2
                segs = [((x, y0), (x+s, ym-gap/2)), ((x+s, ym+gap/2), (x, y0+h))]
            for (ax, ay), (bx, by) in segs:
                # auf Rechteck beschneiden
                if max(ax, bx) < x0 or min(ax, bx) > x0+w:
                    continue
                def clip(px, py, qx, qy):
                    t0, t1 = 0.0, 1.0
                    dx = qx-px
                    if dx != 0:
                        for edge in (x0, x0+w):
                            t = (edge-px)/dx
                            if 0 <= t <= 1:
                                if (px + 0.0001*dx) < edge and dx > 0 and edge == x0: t0 = max(t0, t)
                                if dx > 0 and edge == x0+w: t1 = min(t1, t)
                                if dx < 0 and edge == x0: t1 = min(t1, t)
                                if dx < 0 and edge == x0+w: t0 = max(t0, t)
                    if dx == 0 and not (x0 <= px <= x0+w):
                        return None
                    if t0 >= t1:
                        return None
                    return (px+t0*dx, py+t0*(qy-py), px+t1*dx, py+t1*(qy-py))
                c = clip(ax, ay, bx, by)
                if c:
                    b += f'<line x1="{c[0]:.1f}" y1="{c[1]:.1f}" x2="{c[2]:.1f}" y2="{c[3]:.1f}" stroke="{INK}" stroke-width="1.6"/>'
        if kind == "double":
            ym = y0 + h/2
            b += f'<rect x="{x0}" y="{ym-7}" width="{w}" height="14" fill="#fff" stroke="{INK}" stroke-width="1.5"/>'
        # Welle
        b += f'<line x1="30" y1="{y0+h/2}" x2="{W-30}" y2="{y0+h/2}" {AX}/>'
    save(name, W, H, b)


flank_pair("zahnrad_gerade.svg", "straight")
flank_pair("zahnrad_schraeg.svg", "helical")
flank_pair("zahnrad_pfeil.svg", "herring")
flank_pair("zahnrad_doppelschraeg.svg", "double")

# Kegelradpaar / bevel gear pair (Seitenansicht, Achsen unter 90°)
ax_, ay_ = 210, 210
s1, s2 = 50, 95
b = ""
b += f'<rect x="{ax_-16}" y="15" width="32" height="{ay_-s2-15}" fill="#fff" stroke="{INK}" stroke-width="2"/>'
b += f'<rect x="15" y="{ay_-16}" width="{ax_-s2-15}" height="32" fill="#fff" stroke="{INK}" stroke-width="2"/>'
g1 = [(ax_-s1, ay_-s1), (ax_+s1, ay_-s1), (ax_+s2, ay_-s2), (ax_-s2, ay_-s2)]
g2 = [(ax_-s1, ay_-s1), (ax_-s1, ay_+s1), (ax_-s2, ay_+s2), (ax_-s2, ay_-s2)]
def poly(pts, fill):
    return '<path d="M' + " L".join(f"{x},{y}" for x, y in pts) + f' Z" fill="{fill}" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>'
b += poly(g1, "#ebf7fd") + poly(g2, "#bfe5f7")
for k in range(1, 9):
    t = k/9
    b += f'<line x1="{ax_-s1+2*s1*t:.1f}" y1="{ay_-s1}" x2="{ax_-s2+2*s2*t:.1f}" y2="{ay_-s2}" stroke="{INK}" stroke-width="1.3"/>'
    b += f'<line x1="{ax_-s1}" y1="{ay_-s1+2*s1*t:.1f}" x2="{ax_-s2}" y2="{ay_-s2+2*s2*t:.1f}" stroke="{INK}" stroke-width="1.3"/>'
b += f'<line x1="{ax_}" y1="8" x2="{ax_}" y2="{ay_+30}" {AX}/>'
b += f'<line x1="8" y1="{ay_}" x2="{ax_+30}" y2="{ay_}" {AX}/>'
b += f'<line x1="{ax_-s2-10}" y1="{ay_-s2-10}" x2="{ax_}" y2="{ay_}" stroke="{BLUE}" stroke-width="1.5" stroke-dasharray="5 3"/>'
save("zahnrad_kegelrad.svg", 330, 320, b)

# Schneckengetriebe / worm gear: Schnecke horizontal vor Schneckenrad (Vorderansicht)
W, H = 320, 280
b = f'<path d="{toothed(160, 170, 80, 92, 30, rot=0.05)}" {GEAR}/>'
b += f'<circle cx="160" cy="170" r="22" fill="#fff" stroke="{INK}" stroke-width="2"/>'
b += f'<rect x="40" y="58" width="240" height="40" rx="4" fill="#bfe5f7" stroke="{INK}" stroke-width="2"/>'
for i in range(-2, 17):
    x = 40 + i*16
    xa, xb = x, x+12
    if xb < 40 or xa > 280:
        continue
    xa2, xb2 = max(xa, 40), min(xb, 280)
    ya = 58 + (xa2-xa)/12*40
    yb = 58 + (xb2-xa)/12*40
    b += f'<line x1="{xa2:.1f}" y1="{ya:.1f}" x2="{xb2:.1f}" y2="{yb:.1f}" stroke="{INK}" stroke-width="1.6"/>'
b += f'<line x1="15" y1="78" x2="305" y2="78" {AX}/>'
b += f'<line x1="160" y1="150" x2="160" y2="190" {AX}/><line x1="140" y1="170" x2="180" y2="170" {AX}/>'
save("zahnrad_schnecke.svg", W, H, b)

# Hohlrad mit Ritzel / internal gear
W, H = 300, 300
b = f'<circle cx="150" cy="150" r="130" fill="#ebf7fd" stroke="{INK}" stroke-width="2"/>'
b += f'<path d="{toothed(150, 150, 112, 100, 40)}" fill="#fff" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>'
b += f'<path d="{toothed(150, 197, 42, 53, 15, rot=0.21)}" {GEAR2}/>'
b += f'<circle cx="150" cy="197" r="10" fill="#fff" stroke="{INK}" stroke-width="2"/>'
b += f'<line x1="150" y1="135" x2="150" y2="165" {AX}/><line x1="135" y1="150" x2="165" y2="150" {AX}/>'
save("zahnrad_hohlrad.svg", W, H, b)

# Zahnstange mit Ritzel / rack and pinion
W, H = 340, 260
b = f'<path d="{toothed(170, 100, 58, 72, 16, rot=-math.pi/2 - 0.2)}" {GEAR}/>'
b += f'<circle cx="170" cy="100" r="14" fill="#fff" stroke="{INK}" stroke-width="2"/>'
p = 2*math.pi*65/16
pts = []
x = 10
while x < 330:
    pts += [(x, 172), (x+0.18*p, 172), (x+0.32*p, 172+0) ]
    x += p
rack = "M10,230 L10,190"
x = 10 - 0.1*p
while x < 330:
    rack += f" L{x+0.10*p:.1f},190 L{x+0.25*p:.1f},170 L{x+0.55*p:.1f},170 L{x+0.70*p:.1f},190"
    x += p
rack += " L330,190 L330,230 Z"
b += f'<path d="{rack}" fill="#bfe5f7" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>'
b += f'<rect x="0" y="160" width="10" height="80" fill="#fff"/><rect x="330" y="160" width="10" height="80" fill="#fff"/>'
b += f'<line x1="150" y1="100" x2="190" y2="100" {AX}/><line x1="170" y1="80" x2="170" y2="120" {AX}/>'
save("zahnrad_zahnstange.svg", W, H, b)

# Außen-Stirnradpaar (Vorderansicht)
W, H = 340, 240
b = f'<path d="{toothed(115, 120, 78, 90, 26)}" {GEAR}/>'
b += f'<path d="{toothed(253, 120, 42, 54, 14, rot=0.12)}" {GEAR2}/>'
b += f'<circle cx="115" cy="120" r="16" fill="#fff" stroke="{INK}" stroke-width="2"/><circle cx="253" cy="120" r="10" fill="#fff" stroke="{INK}" stroke-width="2"/>'
save("zahnrad_stirnradpaar.svg", W, H, b)


# ---------- Angestellte Lagerung O / X ----------
def tapered_pair(name, kind):
    W, H, cy = 380, 260, 130
    alpha = math.radians(22)
    up = f'<rect x="20" y="104" width="340" height="52" fill="#f3f3f3" stroke="{INK}" stroke-width="2"/>'
    lines = ""
    for side, xc in ((-1, 110), (1, 270)):
        # Pressure line: bottom shifted outward (O) or inward (X)
        out = side if kind == "O" else -side
        # roller: rotated rectangle, axis tilted so that pressure line (perp.) goes down-outward
        tilt = -out * alpha  # rotation of roller axis
        deg = math.degrees(tilt)
        up += (f'<rect x="{xc-40}" y="20" width="80" height="16" fill="url(#h)" stroke="{INK}" stroke-width="2"/>'
               f'<rect x="{xc-40}" y="88" width="80" height="16" fill="url(#h2)" stroke="{INK}" stroke-width="2"/>'
               f'<g transform="rotate({deg:.1f} {xc} 62)"><path d="M{xc-30},44 L{xc+30},{44+ (6 if out>0 else -6) * 0} L{xc+30},80 L{xc-30},80 Z" fill="none"/></g>'
               f'<g transform="rotate({deg:.1f} {xc} 62)"><rect x="{xc-30}" y="46" width="60" height="32" rx="3" {EL}/></g>')
        # pressure line through roller centre, perpendicular to roller axis
        dx, dy = -math.sin(tilt), math.cos(tilt)
        t0, t1 = -0.0, (cy - 62)/dy
        lines += (f'<line x1="{xc - dx*40:.1f}" y1="{62 - dy*40:.1f}" x2="{xc + dx*t1:.1f}" y2="{cy:.1f}" '
                  f'stroke="{BLUE}" stroke-width="2" stroke-dasharray="6 3"/>')
    body = (up + lines + f'<g transform="translate(0,{2*cy}) scale(1,-1)">{up}{lines}</g>'
            + f'<line x1="5" y1="{cy}" x2="{W-5}" y2="{cy}" {AX}/>')
    save(name, W, H, body)


tapered_pair("lagerung_o.svg", "O")
tapered_pair("lagerung_x.svg", "X")
print("ok", sorted(os.listdir(OUT)))
