"""
GL Data Visualization Handout — reportlab generator
Output: playground/gl-data-vis-handout.pdf
"""
import math
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether, PageBreak
)
from reportlab.platypus.flowables import Flowable
from reportlab.graphics.shapes import (
    Drawing, Line, Rect, Circle, String, PolyLine, Polygon, Group
)

OUT = os.path.join(os.path.dirname(__file__), "gl-data-vis-handout.pdf")

# ── Platypus colors ───────────────────────────────────────────────────────────
INK       = colors.HexColor("#1A1714")
INK2      = colors.HexColor("#2C2823")
INK3      = colors.HexColor("#4F4A42")
INK4      = colors.HexColor("#9A9389")
ACCENT    = colors.HexColor("#1A5A8E")
PAPER     = colors.HexColor("#FFFFFF")
COVERBG   = colors.HexColor("#F3F2EA")
GRIDLINE  = colors.HexColor("#D8D4CC")
RULE      = colors.HexColor("#DDDDDD")
C1        = colors.HexColor("#2F87C8")
C1D       = colors.HexColor("#1A5A8E")
C1L       = colors.HexColor("#B5D5EA")
C2        = colors.HexColor("#CC4948")
C2D       = colors.HexColor("#8A2C2B")
C2L       = colors.HexColor("#E89C9C")
C3        = colors.HexColor("#2AA584")
C3D       = colors.HexColor("#1A6B53")
C3L       = colors.HexColor("#92D6BF")
C4        = colors.HexColor("#7554A3")
C4D       = colors.HexColor("#4A3470")
C4L       = colors.HexColor("#B5A0CC")
C5        = colors.HexColor("#EA822D")
C5D       = colors.HexColor("#A8580F")
C5L       = colors.HexColor("#F4BC8A")
C6        = colors.HexColor("#CDC86B")
C6D       = colors.HexColor("#8A8638")
C6L       = colors.HexColor("#E6E2A8")
CMUTED    = colors.HexColor("#AFB5BE")
CMUTEDD   = colors.HexColor("#5F6773")
CMUTEDL   = colors.HexColor("#CDD2D9")

# Alpha variants used in chart drawings
_C1_80    = colors.Color(0x2F/255, 0x87/255, 0xC8/255, 0.8)
_C1D_80   = colors.Color(0x1A/255, 0x5A/255, 0x8E/255, 0.8)
_C1_25    = colors.Color(0x2F/255, 0x87/255, 0xC8/255, 0.25)
_CM_80    = colors.Color(0xAF/255, 0xB5/255, 0xBE/255, 0.8)
_CMD_80   = colors.Color(0x5F/255, 0x67/255, 0x73/255, 0.8)
_CM_18    = colors.Color(0xAF/255, 0xB5/255, 0xBE/255, 0.18)
_WHT_70   = colors.Color(1, 1, 1, 0.70)

# ── Chart drawing constants ───────────────────────────────────────────────────
CW   = 432    # drawing width (pts) — fits inside 6.5" text block
CH   = 150    # drawing height (pts)
CX0  = 48     # plot left
CY0  = 22     # plot bottom
CPW  = 358    # plot width  → CX1 = 406
CPH  = 112    # plot height → CY1 = 134

HV   = "Helvetica"
HVB  = "Helvetica-Bold"
HVI  = "Helvetica-Oblique"
CFS  = 6.5    # tick / axis label size inside charts
CFSL = 7.5    # direct series labels
CFSS = 5.5    # source line


# ── Chart scale helpers ───────────────────────────────────────────────────────
def cyl(v, vmin, vmax):
    return CY0 + (v - vmin) / (vmax - vmin) * CPH

def cxl(v, vmin, vmax):
    return CX0 + (v - vmin) / (vmax - vmin) * CPW

def cxlog(g, gmin=1000, gmax=40000):
    return CX0 + (math.log10(g) - math.log10(gmin)) / \
           (math.log10(gmax) - math.log10(gmin)) * CPW


# ── Chart drawing helpers ─────────────────────────────────────────────────────
def _mk(w=CW, h=CH):
    return Drawing(w, h)

def _hgrid(d, ys, x0=CX0, x1=CX0+CPW):
    for y in ys:
        d.add(Line(x0, y, x1, y, strokeColor=GRIDLINE, strokeWidth=0.6))

def _vgrid(d, xs, y0=CY0, y1=CY0+CPH):
    for x in xs:
        d.add(Line(x, y0, x, y1, strokeColor=GRIDLINE, strokeWidth=0.6))

def _axes(d, x0=CX0, y0=CY0, x1=CX0+CPW, y1=CY0+CPH):
    d.add(Line(x0, y0, x0, y1, strokeColor=INK2, strokeWidth=0.8))
    d.add(Line(x0, y0, x1, y0, strokeColor=INK2, strokeWidth=0.8))

def _ytick(d, y, label=None, x0=CX0):
    d.add(Line(x0-4, y, x0, y, strokeColor=INK2, strokeWidth=0.6))
    if label is not None:
        d.add(String(x0-6, y-2.3, label, fontName=HV, fontSize=CFS,
                     fillColor=INK3, textAnchor="end"))

def _xtick(d, x, label=None, y0=CY0):
    d.add(Line(x, y0, x, y0-4, strokeColor=INK2, strokeWidth=0.6))
    if label is not None:
        d.add(String(x, y0-4-CFS-0.5, label, fontName=HV, fontSize=CFS,
                     fillColor=INK3, textAnchor="middle"))

def _ylabel(d, text, x0=CX0, cy=(CY0+CY0+CPH)/2):
    s = String(0, 0, text, fontName=HV, fontSize=CFS, fillColor=INK3,
               textAnchor="middle")
    g = Group(s)
    g.transform = (0, 1, -1, 0, 10, cy)
    d.add(g)

def _xlabel(d, text):
    d.add(String((CX0 + CX0+CPW)/2, 2, text, fontName=HV, fontSize=CFS,
                 fillColor=INK3, textAnchor="middle"))

def _src(d, text, w=CW):
    d.add(String(w-2, 1, text, fontName=HVI, fontSize=CFSS,
                 fillColor=INK4, textAnchor="end"))

def _dot(d, cx, cy, r, fill, stroke, sw=0.6):
    d.add(Circle(cx, cy, r, fillColor=fill, strokeColor=stroke, strokeWidth=sw))

def _pl(d, pts, color, sw=1.4):
    flat = [c for p in pts for c in p]
    d.add(PolyLine(flat, strokeColor=color, strokeWidth=sw, strokeLineJoin=1))

def _poly(d, pts, fill, stroke=None, sw=0):
    flat = [c for p in pts for c in p]
    d.add(Polygon(flat, fillColor=fill, strokeColor=stroke or fill, strokeWidth=sw))

def _rect(d, x, y, w, h, fill, stroke=None, sw=0):
    d.add(Rect(x, y, w, h, fillColor=fill,
               strokeColor=stroke or fill, strokeWidth=sw))

def _lbl(d, x, y, text, fill, bold=True, fs=CFSL, anchor="start"):
    d.add(String(x, y, text, fontName=HVB if bold else HV,
                 fontSize=fs, fillColor=fill, textAnchor=anchor))


# ── 1. Scatter ────────────────────────────────────────────────────────────────
def draw_scatter():
    d = _mk()
    _hgrid(d, [cyl(v,-1.5,2.0) for v in [-1.5,-0.5,0.5,1.5]])
    _axes(d)
    for v, l in [(-1.5,"−1.5"),(-.5,"−0.5"),(.5,"0.5"),(1.5,"1.5")]:
        _ytick(d, cyl(v,-1.5,2.0), l)
    for g, l in [(1000,"1k"),(3000,"3k"),(10000,"10k"),(30000,"30k")]:
        _xtick(d, cxlog(g), l)
    _ylabel(d, "ECI", cy=(CY0+CY0+CPH)/2)
    _xlabel(d, "GDP per capita (log scale)")
    muted = [(1200,-1.4),(1500,-.8),(2000,-1.0),(2500,-1.1),(3500,-.3),(4000,.1),
             (5000,-.2),(6000,.5),(8000,.3),(9000,.8),(12000,.9),(15000,1.1),
             (20000,1.3),(25000,1.5),(35000,1.6),(7000,-.6),(11000,.6),(18000,1.0),
             (1700,-1.3),(22000,1.4),(4500,-.05)]
    for g, ec in muted:
        _dot(d, cxlog(g), cyl(ec,-1.5,2.0), 3.0, _CM_80, _CMD_80, sw=0.5)
    fx, fy = cxlog(1800), cyl(0.55,-1.5,2.0)
    _dot(d, fx, fy, 4.0, _C1_80, _C1D_80, sw=0.7)
    _lbl(d, fx+6, fy-2.5, "PAK", C1D)
    _src(d, "Source: Atlas of Economic Complexity")
    return d


# ── 2. Line ───────────────────────────────────────────────────────────────────
def draw_line():
    d = _mk()
    N = 9
    xs = [CX0 + i/(N-1)*CPW for i in range(N)]
    yrs = list(range(2016, 2025))
    _hgrid(d, [cyl(v,8,22) for v in [10,14,18,22]])
    _axes(d)
    for v in [10,14,18,22]:
        _ytick(d, cyl(v,8,22), str(v)+"%")
    for i in [0,2,4,6,8]:
        _xtick(d, xs[i], str(yrs[i]))
    _ylabel(d, "Exports / GDP")
    mS = [[13,14,13.5,14,12,14.5,15,14.5,15.2],[18,17,16,15,14,16,17,16,16.5],
          [20,19,18,17,15,17,18,17.5,17.8],[10,11,10.5,11,9,10,11,10.5,11]]
    mL = ["IND","BGD","LKA","NPL"]
    for vals, ml in zip(mS, mL):
        _pl(d, [(xs[i], cyl(v,8,22)) for i,v in enumerate(vals)], CMUTED, sw=1.1)
        d.add(String(CX0+CPW+4, cyl(vals[-1],8,22)-2.3, ml, fontName=HV,
                     fontSize=CFSS, fillColor=CMUTEDD, textAnchor="start"))
    pak = [14,13,13.5,12,10,13.5,15.5,16,17.5]
    _pl(d, [(xs[i], cyl(v,8,22)) for i,v in enumerate(pak)], C1, sw=2.0)
    _lbl(d, CX0+CPW+4, cyl(pak[-1],8,22)-2.5, "PAK", C1D)
    _src(d, "Source: World Bank WDI")
    return d


# ── 3. Horizontal bar ─────────────────────────────────────────────────────────
def draw_bar():
    d = _mk()
    LX0, LX1, LY0, LY1 = 74, 408, 12, CH-10
    LPW = LX1 - LX0
    data = [("Textiles",58,True),("Food & agri",14,False),("Chemicals",7,False),
            ("Leather",6,False),("Sports",5,False),("Engineering",4,False),
            ("Gems",3,False),("Other",3,False)]
    N = len(data)
    bH, gap = 11, 7
    tot = (bH+gap)*N - gap
    y0b = LY0 + (LY1-LY0-tot)/2
    def xv(v): return LX0 + v/65*LPW
    # vertical gridlines
    for v in [0,20,40,60]:
        d.add(Line(xv(v), LY0, xv(v), LY1,
                   strokeColor=INK2 if v==0 else GRIDLINE,
                   strokeWidth=0.8 if v==0 else 0.6))
        _xtick(d, xv(v), str(v)+"%", y0=LY0)
    d.add(Line(LX0, LY0, LX1, LY0, strokeColor=INK2, strokeWidth=0.8))
    for i,(label,val,focus) in enumerate(data):
        y = y0b + (N-1-i)*(bH+gap)
        bw = val/65*LPW
        _rect(d, LX0, y, bw, bH, C1 if focus else CMUTED)
        d.add(String(LX0-3, y+bH*0.35, label, fontName=HV, fontSize=CFS,
                     fillColor=INK3, textAnchor="end"))
        d.add(String(LX0+bw+3, y+bH*0.35, str(val)+"%", fontName=HVB, fontSize=CFS,
                     fillColor=C1D if focus else CMUTEDD, textAnchor="start"))
    _src(d, "Source: Pakistan PBS 2024")
    return d


# ── 4. Stacked bar ────────────────────────────────────────────────────────────
def draw_stacked_bar():
    d = _mk()
    yrs = [2018,2019,2020,2021,2022,2023]
    clrs = [C1,C2,C3]; dks = [C1D,C2D,C3D]; cats = ["Manufactures","Agriculture","Services"]
    vals = [[62,22,16],[60,22,18],[57,21,22],[58,21,21],[59,20,21],[56,19,25]]
    N = len(yrs); bW, gp = 38, 14
    tot = (bW+gp)*N - gp
    x0b = CX0 + (CPW-tot)/2
    _hgrid(d, [cyl(v,0,100) for v in [25,50,75,100]])
    _axes(d)
    for v in [0,25,50,75,100]:
        _ytick(d, cyl(v,0,100), str(v)+"%")
    _ylabel(d, "Export share")
    for i, row in enumerate(vals):
        bx = x0b + i*(bW+gp)
        cy = CY0
        for j, pct in enumerate(row):
            h = pct/100*CPH
            _rect(d, bx, cy, bW, h, clrs[j], stroke=PAPER, sw=0.6)
            cy += h
        _xtick(d, bx+bW/2, str(yrs[i]))
    # legend top-right
    lx, ly = CX0+CPW-4, CY0+CPH-6
    for i,(cat,clr,dk) in enumerate(zip(cats,clrs,dks)):
        ry = ly - i*11
        _rect(d, lx-56, ry-5.5, 7, 7, clr)
        d.add(String(lx-46, ry-1.5, cat, fontName=HV, fontSize=CFSS,
                     fillColor=dk, textAnchor="start"))
    _src(d, "Source: UN Comtrade")
    return d


# ── 5. Treemap ────────────────────────────────────────────────────────────────
def draw_treemap():
    W, H = CW, CH
    d = Drawing(W, H)
    # tiles defined as (tx, ty_from_top, tw, th, label, share, focus)
    tiles = [
        (1,  1, 117, 76, "Knitwear",    "24%", True),
        (1, 79, 117, 69, "Woven cotton","19%", True),
        (120, 1,  73, 52, "Bed linen",  "12%", False),
        (120,55,  73, 50, "Cotton yarn","11%", False),
        (195, 1, 100, 38, "Rice",       "8%",  False),
        (195,41,  49, 46, "Leather",    "5%",  False),
        (246,41,  49, 46, "Sports",     "5%",  False),
        (195,89,  72, 59, "Chemicals",  "7%",  False),
        (269,89,  26, 59, "Other",      "4%",  False),
        (120,107,  73, 41, "Surgical",  "5%",  False),
    ]
    for tx, ty_top, tw, th, label, share, focus in tiles:
        ty = H - ty_top - th
        fill = C1 if focus else CMUTED
        tf   = PAPER if focus else INK2
        sf   = _WHT_70 if focus else INK3
        _rect(d, tx+0.5, ty+0.5, tw-1, th-1, fill)
        if tw > 38 and th > 20:
            fs = min(CFSL+1, tw/7.5)
            d.add(String(tx+5, ty+th-fs-3, label, fontName=HVB,
                         fontSize=fs, fillColor=tf, textAnchor="start"))
            if th > 34:
                d.add(String(tx+5, ty+th-fs*2-4, share, fontName=HV,
                             fontSize=fs*0.82, fillColor=sf, textAnchor="start"))
    _src(d, "Source: Pakistan PBS / UN Comtrade 2023", w=W)
    return d


# ── 6. Boxplot ────────────────────────────────────────────────────────────────
def draw_boxplot():
    d = _mk()
    yrs = [2019,2020,2021,2022,2023]; N = len(yrs)
    xs = [CX0 + (i+0.5)/N*CPW for i in range(N)]
    _hgrid(d, [cyl(v,0,24000) for v in [5000,10000,15000,20000]])
    _axes(d)
    for v,l in [(0,"$0"),(5000,"$5k"),(10000,"$10k"),(15000,"$15k"),(20000,"$20k")]:
        _ytick(d, cyl(v,0,24000), l)
    for i,yr in enumerate(yrs): _xtick(d, xs[i], str(yr))
    _ylabel(d, "GDP per capita")
    boxes = [(1200,2500,5000,12000,21000),(1150,2400,4800,11500,20500),
             (1200,2600,5200,12500,21500),(1300,2700,5500,13000,22000),
             (1250,2650,5300,12800,21800)]
    BW = 20
    for i,(p10,q1,med,q3,p90) in enumerate(boxes):
        cx = xs[i]
        yp10,yp90 = cyl(p10,0,24000),cyl(p90,0,24000)
        yq1,yq3,ymed = cyl(q1,0,24000),cyl(q3,0,24000),cyl(med,0,24000)
        d.add(Line(cx, yp10, cx, yp90, strokeColor=CMUTED, strokeWidth=0.8))
        for yw in [yp10, yp90]:
            d.add(Line(cx-4, yw, cx+4, yw, strokeColor=CMUTED, strokeWidth=0.8))
        _rect(d, cx-BW/2, yq1, BW, yq3-yq1, CMUTEDL, stroke=CMUTED, sw=0.8)
        d.add(Line(cx-BW/2, ymed, cx+BW/2, ymed, strokeColor=CMUTEDD, strokeWidth=1.2))
    pak = [1520,1430,1510,1580,1550]
    _pl(d, [(xs[i], cyl(v,0,24000)) for i,v in enumerate(pak)], C1, sw=2.0)
    for i,v in enumerate(pak):
        _dot(d, xs[i], cyl(v,0,24000), 3.0, _C1_80, _C1D_80, sw=0.5)
    _lbl(d, xs[-1]+6, cyl(pak[-1],0,24000)-2.5, "PAK", C1D)
    _src(d, "Source: World Bank WDI")
    return d


# ── 7. Radar ──────────────────────────────────────────────────────────────────
def draw_radar():
    W, H = CW, CH
    d = Drawing(W, H)
    cx, cy, R = W/2 - 18, H/2 + 2, 56
    dims = ["Complexity","Diversity","Fitness","Education","Infrastructure","Market size"]
    N = len(dims)
    def ang(i): return i/N*2*math.pi - math.pi/2
    def pt(r, i): return (cx + r*math.cos(ang(i)), cy + r*math.sin(ang(i)))
    # grid rings (closed polylines)
    for f in [0.25, 0.5, 0.75, 1.0]:
        ring = [pt(f*R, i) for i in range(N)] + [pt(f*R, 0)]
        _pl(d, ring, GRIDLINE, sw=0.5)
    # spokes
    for i in range(N):
        px, py = pt(R, i)
        d.add(Line(cx, cy, px, py, strokeColor=GRIDLINE, strokeWidth=0.5))
    # peer (muted) polygon
    peer = [.52,.58,.45,.55,.50,.65]
    _poly(d, [pt(v*R, i) for i,v in enumerate(peer)], _CM_18, stroke=CMUTED, sw=1.2)
    # pak polygon
    pak = [.42,.48,.40,.38,.32,.55]
    _poly(d, [pt(v*R, i) for i,v in enumerate(pak)], _C1_25, stroke=C1, sw=1.8)
    # pak dots
    for i,v in enumerate(pak):
        _dot(d, *pt(v*R, i), 2.5, C1, C1D, sw=0.4)
    # dimension labels
    for i, dim in enumerate(dims):
        px, py = pt(R+12, i)
        anchor = "end" if px < cx-5 else ("start" if px > cx+5 else "middle")
        d.add(String(px, py-2, dim, fontName=HV, fontSize=CFSS,
                     fillColor=INK3, textAnchor=anchor))
    # legend
    lx, ly = cx+R+20, cy+10
    d.add(Line(lx, ly, lx+11, ly, strokeColor=C1, strokeWidth=1.8))
    d.add(String(lx+14, ly-2, "PAK", fontName=HVB, fontSize=CFSS,
                 fillColor=C1D, textAnchor="start"))
    d.add(Line(lx, ly-11, lx+11, ly-11, strokeColor=CMUTED, strokeWidth=1.2))
    d.add(String(lx+14, ly-13, "Peer avg.", fontName=HV, fontSize=CFSS,
                 fillColor=CMUTEDD, textAnchor="start"))
    _src(d, "Source: WEF / World Bank", w=W)
    return d


# ── 8. Choropleth (tile grid) ─────────────────────────────────────────────────
def draw_choropleth():
    W, H = CW, CH
    d = Drawing(W, H)
    data = [("IND",0.78),("LKA",0.41),("IRN",0.45),("BGD",0.32),
            ("KAZ",0.35),("UZB",0.10),("PAK",0.12),("MMR",-0.05),
            ("BTN",0.05),("MDV",0.22),("NPL",-0.18),("AFG",-0.85)]
    ramp = [colors.HexColor(h) for h in
            ["#DDE9F4","#B5D5EA","#7FB8DB","#4A99C6","#2F87C8","#1A5A8E"]]
    light = {ramp[0], ramp[1]}
    def cfill(v):
        t = max(0.0, min(1.0, (v+1)/2))
        return ramp[min(5, int(t*6))]
    cols, tW, tH, gp = 4, 68, 30, 2
    rows = math.ceil(len(data)/cols)
    tot = cols*(tW+gp) - gp
    ox, oy_top = (W-tot)/2, 10
    for idx, (code, val) in enumerate(data):
        col, row = idx%cols, idx//cols
        tx = ox + col*(tW+gp)
        ty = H - oy_top - (row+1)*(tH+gp) + gp
        fill = cfill(val)
        tf = INK2 if fill in light else PAPER
        _rect(d, tx, ty, tW, tH, fill)
        d.add(String(tx+tW/2, ty+tH*0.56, code, fontName=HVB, fontSize=7,
                     fillColor=tf, textAnchor="middle"))
        sign = "+" if val > 0 else ""
        d.add(String(tx+tW/2, ty+tH*0.22, f"{sign}{val:.2f}", fontName=HV,
                     fontSize=5.5, fillColor=tf, textAnchor="middle"))
    # legend bar
    lbar_top = oy_top + rows*(tH+gp) + 6
    lby = H - lbar_top - 6
    step = tot/6
    for i, clr in enumerate(ramp):
        _rect(d, ox+i*step, lby, step, 6, clr)
    d.add(String(ox, lby-7, "Lower complexity", fontName=HV, fontSize=CFSS,
                 fillColor=INK4, textAnchor="start"))
    d.add(String(ox+tot, lby-7, "Higher complexity", fontName=HV, fontSize=CFSS,
                 fillColor=INK4, textAnchor="end"))
    _src(d, "Source: Atlas of Economic Complexity", w=W)
    return d


# ── Color swatch flowable ─────────────────────────────────────────────────────
class ColorSwatch(Flowable):
    def __init__(self, color, width=14, height=14):
        super().__init__()
        self.color = color
        self.width = width
        self.height = height

    def draw(self):
        self.canv.setFillColor(self.color)
        self.canv.rect(0, 0, self.width, self.height, fill=1, stroke=0)


# ── Page templates ────────────────────────────────────────────────────────────
def on_page(canvas, doc):
    canvas.saveState()
    w, h = letter
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(0.5)
    canvas.line(0.75*inch, 0.6*inch, w-0.75*inch, 0.6*inch)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(INK4)
    canvas.drawRightString(w-0.75*inch, 0.42*inch, str(doc.page))
    if doc.page > 1:
        canvas.drawString(0.75*inch, 0.42*inch, "Growth Lab — Data Visualization Guide")
    canvas.restoreState()

def on_cover_page(canvas, doc):
    pass  # plain white, no decorations


# ── Styles ────────────────────────────────────────────────────────────────────
def make_styles():
    return {
        "section_num": ParagraphStyle("section_num", fontName="Helvetica-Bold",
            fontSize=9, textColor=ACCENT, spaceBefore=22, spaceAfter=2, letterSpacing=1.2),
        "section_head": ParagraphStyle("section_head", fontName="Helvetica-Bold",
            fontSize=18, leading=22, textColor=INK, spaceBefore=2, spaceAfter=10),
        "sub_head": ParagraphStyle("sub_head", fontName="Helvetica-Bold",
            fontSize=12, leading=16, textColor=INK, spaceBefore=14, spaceAfter=5),
        "sub_head_accent": ParagraphStyle("sub_head_accent", fontName="Helvetica-Bold",
            fontSize=10, leading=14, textColor=ACCENT, spaceBefore=12, spaceAfter=4,
            letterSpacing=0.5),
        "body": ParagraphStyle("body", fontName="Helvetica", fontSize=10,
            leading=15, textColor=INK2, spaceAfter=6),
        "bullet": ParagraphStyle("bullet", fontName="Helvetica", fontSize=10,
            leading=14, textColor=INK2, leftIndent=14, spaceAfter=4, bulletIndent=4),
        "caption": ParagraphStyle("caption", fontName="Helvetica-Oblique", fontSize=9,
            leading=13, textColor=INK3, spaceAfter=4, alignment=TA_CENTER),
        "code": ParagraphStyle("code", fontName="Courier", fontSize=8.5, leading=13,
            textColor=INK3, backColor=colors.HexColor("#F4F1EA"),
            leftIndent=10, rightIndent=10, spaceAfter=6),
        "rule_num": ParagraphStyle("rule_num", fontName="Helvetica-Bold", fontSize=10,
            leading=14, textColor=ACCENT, spaceBefore=8, spaceAfter=2),
        "chart_eyebrow": ParagraphStyle("chart_eyebrow", fontName="Helvetica-Bold",
            fontSize=8, textColor=ACCENT, spaceBefore=4, spaceAfter=2,
            letterSpacing=0.8, alignment=TA_CENTER),
    }

S = make_styles()


# ── Helpers ───────────────────────────────────────────────────────────────────
def rule_line(color=RULE, thickness=0.5):
    return HRFlowable(width="100%", thickness=thickness, color=color,
                      spaceAfter=8, spaceBefore=4)

def section_header(num, title):
    return [rule_line(ACCENT, 1.5),
            Paragraph(f"SECTION {num}", S["section_num"]),
            Paragraph(title, S["section_head"])]

def sub(title):
    return Paragraph(title, S["sub_head"])

def subaccent(title):
    return Paragraph(title.upper(), S["sub_head_accent"])

def body(text):
    return Paragraph(text, S["body"])

def bullet(text):
    return Paragraph(f"<bullet>–</bullet> {text}", S["bullet"])

def sp(h=6):
    return Spacer(1, h)

def chart_sample(drawing, caption):
    drawing.hAlign = "CENTER"
    return [
        sp(6),
        drawing,
        Paragraph(caption, S["caption"]),
        sp(4),
    ]


# ── Palette table ─────────────────────────────────────────────────────────────
def palette_table():
    h  = ParagraphStyle("th", fontName="Helvetica-Bold", fontSize=9, textColor=INK, leading=12)
    c  = ParagraphStyle("td", fontName="Helvetica",      fontSize=9, textColor=INK2, leading=12)
    mo = ParagraphStyle("mn", fontName="Courier",        fontSize=8.5, textColor=INK3, leading=12)
    palette = [
        ("c-1","Blue",  C1L,"#B5D5EA",C1, "#2F87C8",C1D,"#1A5A8E","Primary / single-series default"),
        ("c-2","Red",   C2L,"#E89C9C",C2, "#CC4948",C2D,"#8A2C2B","Contrast / lead finding"),
        ("c-3","Teal",  C3L,"#92D6BF",C3, "#2AA584",C3D,"#1A6B53","Third series"),
        ("c-4","Purple",C4L,"#B5A0CC",C4, "#7554A3",C4D,"#4A3470","Fourth series"),
        ("c-5","Orange",C5L,"#F4BC8A",C5, "#EA822D",C5D,"#A8580F","Fifth series"),
        ("c-6","Yellow",C6L,"#E6E2A8",C6, "#CDC86B",C6D,"#8A8638","Sixth series"),
        ("c-muted","Grey",CMUTEDL,"#CDD2D9",CMUTED,"#AFB5BE",CMUTEDD,"#5F6773","De-emphasis / everyone else"),
    ]
    col_w = [0.45*inch,0.45*inch,0.18*inch,0.72*inch,0.18*inch,0.72*inch,0.18*inch,0.72*inch,1.6*inch]
    data = [[Paragraph("Token",h),Paragraph("Name",h),Paragraph("",h),Paragraph("Light",h),
             Paragraph("",h),Paragraph("Main",h),Paragraph("",h),Paragraph("Dark",h),Paragraph("Role",h)]]
    for tok,name,cl,hl,cm,hm,cd,hd,role in palette:
        data.append([Paragraph(tok,mo),Paragraph(name,c),ColorSwatch(cl,14,14),Paragraph(hl,mo),
                     ColorSwatch(cm,14,14),Paragraph(hm,mo),ColorSwatch(cd,14,14),Paragraph(hd,mo),Paragraph(role,c)])
    tbl = Table(data, colWidths=col_w, repeatRows=1)
    tbl.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#F4F1EA")),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[PAPER,colors.HexColor("#FAFAF8")]),
        ("LINEBELOW",(0,0),(-1,0),0.75,INK2),("LINEBELOW",(0,-1),(-1,-1),0.5,RULE),
        ("LINEBEFORE",(0,0),(0,-1),0.5,RULE),("LINEAFTER",(-1,0),(-1,-1),0.5,RULE),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),("TOPPADDING",(0,0),(-1,-1),5),
        ("BOTTOMPADDING",(0,0),(-1,-1),5),("LEFTPADDING",(0,0),(-1,-1),5),
        ("RIGHTPADDING",(0,0),(-1,-1),5),
    ]))
    return tbl


# ── Typography table ──────────────────────────────────────────────────────────
def typo_table():
    h = ParagraphStyle("th",fontName="Helvetica-Bold",fontSize=9,textColor=INK,leading=12)
    c = ParagraphStyle("td",fontName="Helvetica",fontSize=9,textColor=INK2,leading=12)
    m = ParagraphStyle("mn",fontName="Courier",fontSize=8,textColor=INK3,leading=12)
    rows = [["Element","Family","Size","Weight","Color","Notes"],
            ["Figure label","Inter","12px","600","#1A5A8E","UPPERCASE, 0.14em tracking"],
            ["Chart title","Source Serif 4","14px","500","#1A1714","Ends in a period — states a finding"],
            ["Chart subtitle","Inter","12px","400","#4F4A42","Does not end in a period"],
            ["Axis label","Inter","12px","500","#2C2823","Y rotated −90°; omit for year axis"],
            ["Axis tick label","Inter","12px","400","#2C2823","tabular-nums always"],
            ["Series label","Inter","12px","600","c-N-dark","Dark tone of series color (WCAG AA)"],
            ["Chart source","Source Serif 4 italic","12px","—","#2C2823","Always required, below chart"]]
    col_w = [1.1*inch,1.2*inch,0.5*inch,0.6*inch,0.75*inch,2.1*inch]
    styled = []
    for i, row in enumerate(rows):
        styled.append([Paragraph(cell, h if i==0 else (m if j==4 and i>0 else c))
                       for j,cell in enumerate(row)])
    tbl = Table(styled, colWidths=col_w, repeatRows=1)
    tbl.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#F4F1EA")),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[PAPER,colors.HexColor("#FAFAF8")]),
        ("LINEBELOW",(0,0),(-1,0),0.75,INK2),("LINEBELOW",(0,-1),(-1,-1),0.5,RULE),
        ("LINEBEFORE",(0,0),(0,-1),0.5,RULE),("LINEAFTER",(-1,0),(-1,-1),0.5,RULE),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),("TOPPADDING",(0,0),(-1,-1),5),
        ("BOTTOMPADDING",(0,0),(-1,-1),5),("LEFTPADDING",(0,0),(-1,-1),5),
        ("RIGHTPADDING",(0,0),(-1,-1),5),
    ]))
    return tbl


# ── Decision rules table ──────────────────────────────────────────────────────
def decision_rules_table():
    h = ParagraphStyle("th",fontName="Helvetica-Bold",fontSize=9,textColor=INK,leading=12)
    n = ParagraphStyle("num",fontName="Helvetica-Bold",fontSize=9,textColor=ACCENT,leading=12)
    c = ParagraphStyle("td",fontName="Helvetica",fontSize=9,textColor=INK2,leading=13)
    rules = [
        ("1","Seven-color palette including muted.","Colors added in order — c-1, c-2, c-3 … Use all six categorical colors only when absolutely necessary. More than six → re-think the chart type."),
        ("2","Dark tone for strokes and all text.","Scatter strokes use the dark version of the fill. Every direct label, legend entry, callout, and annotation also uses the dark tone. This includes muted series: c-muted lines/bars → c-muted-dark labels. Main tones do all the fill work. (WCAG AA.)"),
        ("3","Overlapping marks get 0.8 opacity.","Scatter circles, area bands, overlaid polygons: fill-opacity 0.8 and stroke-opacity 0.8. Single-layer marks (bars, treemap, choropleth) stay full opacity."),
        ("4","Axis line and ticks are 1px #2C2823.","Ticks 4px long, outward, never inward."),
        ("5","Gridlines are 1px #D8D4CC.","Only where the reader needs to estimate off the axis; never both X and Y unless the chart is dense. Horizontal-bar charts put gridlines on X."),
        ("6","Axis labels: Inter 12px / 500 / #2C2823.","Tick labels: Inter 12px / 400 / #2C2823 with tabular-nums."),
        ("7","Color encodes meaning, not decoration.","If a color is not earning its keep, remove it."),
        ("8","Implement the pop-up effect whenever possible.","Paint supporting data in c-muted (#AFB5BE) and reserve a saturated hue for the 1–2 series the reader must track."),
        ("9","Sequential ramp for ordered values.","Diverging only with a meaningful midpoint (gains vs. losses, above/below baseline). Never diverging for purely positive scales."),
        ("10","Chart title ends with a period.","It reads as a finding statement. The subtitle does not end in a period."),
        ("11","No monospace.","All numerals use Inter with font-variant-numeric: tabular-nums."),
    ]
    data = [[Paragraph("#",h),Paragraph("Rule",h),Paragraph("Detail",h)]]
    for num,rule,detail in rules:
        data.append([Paragraph(num,n),Paragraph(f"<b>{rule}</b>",c),Paragraph(detail,c)])
    col_w = [0.3*inch,1.8*inch,4.4*inch]
    tbl = Table(data, colWidths=col_w, repeatRows=1)
    tbl.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#F4F1EA")),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[PAPER,colors.HexColor("#FAFAF8")]),
        ("LINEBELOW",(0,0),(-1,0),0.75,INK2),("LINEBELOW",(0,-1),(-1,-1),0.5,RULE),
        ("LINEBEFORE",(0,0),(0,-1),0.5,RULE),("LINEAFTER",(-1,0),(-1,-1),0.5,RULE),
        ("VALIGN",(0,0),(-1,-1),"TOP"),("TOPPADDING",(0,0),(-1,-1),6),
        ("BOTTOMPADDING",(0,0),(-1,-1),6),("LEFTPADDING",(0,0),(-1,-1),6),
        ("RIGHTPADDING",(0,0),(-1,-1),6),
    ]))
    return tbl


# ── Chart rule block ──────────────────────────────────────────────────────────
def chart_rule_block(title, color, rules, note=None):
    bullet_s = ParagraphStyle("cb", fontName="Helvetica", fontSize=9.5,
                               leading=14, textColor=INK2, leftIndent=14,
                               spaceAfter=3, bulletIndent=4)
    note_s   = ParagraphStyle("cn", fontName="Helvetica-Oblique", fontSize=8.5,
                               leading=12, textColor=INK4, leftIndent=14, spaceAfter=0)
    items = []
    for r in rules:
        items.append(Paragraph(f"<bullet>–</bullet> {r}", bullet_s))
    if note:
        items.append(sp(2))
        items.append(Paragraph(f"Note: {note}", note_s))
    return items


# ── Ink ramp table ────────────────────────────────────────────────────────────
def ink_table():
    c = ParagraphStyle("td",fontName="Helvetica",fontSize=9,textColor=INK2,leading=12)
    m = ParagraphStyle("mn",fontName="Courier",fontSize=9,textColor=INK3,leading=12)
    rows = [
        (INK,    "ink",     "#1A1714","Chart title, strong emphasis"),
        (INK2,   "ink-2",   "#2C2823","Axis line, axis labels, tick labels, annotations"),
        (INK3,   "ink-3",   "#4F4A42","Subtitles, secondary captions"),
        (ACCENT, "accent",  "#1A5A8E","Figure labels, eyebrows, links — non-data chrome only"),
        (GRIDLINE,"gridline","#D8D4CC","Major gridlines inside the plot area"),
    ]
    col_w = [0.28*inch,0.7*inch,0.8*inch,4.7*inch]
    data = []
    for clr, tok, hex_, role in rows:
        data.append([ColorSwatch(clr,14,14),Paragraph(tok,m),Paragraph(hex_,m),Paragraph(role,c)])
    tbl = Table(data, colWidths=col_w)
    tbl.setStyle(TableStyle([
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),("TOPPADDING",(0,0),(-1,-1),5),
        ("BOTTOMPADDING",(0,0),(-1,-1),5),("LEFTPADDING",(0,0),(-1,-1),4),
        ("RIGHTPADDING",(0,0),(-1,-1),6),
        ("ROWBACKGROUNDS",(0,0),(-1,-1),[PAPER,colors.HexColor("#FAFAF8")]),
        ("LINEBEFORE",(0,0),(0,-1),0.5,RULE),("LINEAFTER",(-1,0),(-1,-1),0.5,RULE),
        ("LINEBELOW",(0,-1),(-1,-1),0.5,RULE),
    ]))
    return tbl


# ── Build ─────────────────────────────────────────────────────────────────────
def build():
    doc = SimpleDocTemplate(
        OUT, pagesize=letter,
        leftMargin=0.85*inch, rightMargin=0.85*inch,
        topMargin=0.85*inch,  bottomMargin=0.85*inch,
        title="Growth Lab Data Visualization Guide",
        author="Growth Lab, Harvard Kennedy School",
    )
    story = []

    # ── COVER ────────────────────────────────────────────────────────────────
    story.append(Spacer(1, 3.2*inch))
    story.append(Paragraph("Growth Lab Data Visualization Guide",
        ParagraphStyle("ct", fontName="Helvetica-Bold", fontSize=36, leading=44,
                       textColor=INK, spaceAfter=0)))
    story.append(PageBreak())

    # ── S1: FOUNDATIONS ──────────────────────────────────────────────────────
    story += section_header("1", "Foundations")
    story.append(body("Every GL chart is built from <b>two type families</b> and a "
        "<b>small ink ramp</b>. Resist adding a third family or new neutrals."))
    story.append(sub("Type families"))
    story.append(body("<b>Source Serif 4</b> (serif) — chart title and chart source only. "
        "Title: 14px / weight 500 / #1A1714, always ends in a period."))
    story.append(body("<b>Inter</b> (sans-serif) — everything else inside the figure. "
        "Always use tabular-nums on numeric content."))
    story.append(sub("Chart typography"))
    story.append(typo_table())
    story.append(sub("Ink ramp"))
    story.append(ink_table())
    story.append(sub("Axes, ticks, and gridlines"))
    for t in ["Axis line and ticks: 1px solid #2C2823. Ticks 4px long, pointing outward — never inward.",
              "Tick label sits 6px outside the axis. Axis label sits 20px from the widest tick.",
              "Y-axis label is always rotated −90°, centered on the axis. Never horizontal.",
              "When the X axis shows only years, omit the axis label — the ticks already name the dimension.",
              "Zero baseline drawn at axis weight (1px ink-2), never at gridline weight.",
              "Gridlines: horizontal only by default; never both X and Y unless the chart is very dense."]:
        story.append(bullet(t))
    story.append(sub("Decision rules"))
    story.append(decision_rules_table())
    story.append(PageBreak())

    # ── S2: COLOR ────────────────────────────────────────────────────────────
    story += section_header("2", "Color")
    story.append(sub("Categorical palette"))
    story.append(body("Seven categorical hues (six colors + one muted), each in three tones: "
        "<b>light / main / dark</b>. Colors are assigned in order — c-1 first, then c-2, c-3 …"))
    story.append(palette_table())
    story.append(sp(8))
    story.append(sub("Three tones, three jobs"))
    h = ParagraphStyle("th",fontName="Helvetica-Bold",fontSize=9,textColor=INK,leading=12)
    c = ParagraphStyle("td",fontName="Helvetica",fontSize=9,textColor=INK2,leading=12)
    m = ParagraphStyle("mn",fontName="Courier",fontSize=8.5,textColor=INK3,leading=12)
    tone_data = [
        [Paragraph("Tone",h),Paragraph("Job",h),Paragraph("Example",h)],
        [Paragraph("Main",ParagraphStyle("td",fontName="Helvetica-Bold",fontSize=9,textColor=C1D,leading=12)),
         Paragraph("Fills — bars, lines, treemap tiles, scatter circles.",c),Paragraph("Bar fill: #2F87C8",m)],
        [Paragraph("Dark",ParagraphStyle("td",fontName="Helvetica-Bold",fontSize=9,textColor=C1D,leading=12)),
         Paragraph("Strokes on overlapping marks and every text element tied to the series — "
                   "direct labels, end-labels, legend entries, callouts. Applies to muted series too: "
                   "c-muted fills → c-muted-dark labels. (WCAG AA.)",c),Paragraph("Label: #1A5A8E",m)],
        [Paragraph("Light",ParagraphStyle("td",fontName="Helvetica-Bold",fontSize=9,textColor=C1D,leading=12)),
         Paragraph("Backgrounds, faded states, sequential ramp tail, two/three-tone stacked areas.",c),
         Paragraph("Band: #B5D5EA",m)],
    ]
    tt = Table(tone_data, colWidths=[0.7*inch,4.3*inch,1.5*inch], repeatRows=1)
    tt.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),colors.HexColor("#F4F1EA")),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[PAPER,colors.HexColor("#FAFAF8")]),
        ("LINEBELOW",(0,0),(-1,0),0.75,INK2),("LINEBELOW",(0,-1),(-1,-1),0.5,RULE),
        ("LINEBEFORE",(0,0),(0,-1),0.5,RULE),("LINEAFTER",(-1,0),(-1,-1),0.5,RULE),
        ("VALIGN",(0,0),(-1,-1),"TOP"),("TOPPADDING",(0,0),(-1,-1),6),
        ("BOTTOMPADDING",(0,0),(-1,-1),6),("LEFTPADDING",(0,0),(-1,-1),6),
        ("RIGHTPADDING",(0,0),(-1,-1),6),
    ]))
    story.append(tt)
    story.append(sub("Pop-up / mute-then-highlight"))
    story.append(body("Paint supporting data in <b>c-muted (#AFB5BE)</b> and reserve a saturated hue — "
        "usually c-1, sometimes c-1 + c-2 — for the 1–2 series the reader must track."))
    for t in ["Scatter: muted backdrop circles at 0.8 opacity + one focus circle (c-1) painted once.",
              "Line: muted grey lines at 2px + focus line in c-1 at 2.4px.",
              "Bar / treemap: muted grey bars or tiles + focus bar/tile in c-1.",
              "Boxplot: muted-light fill + muted stroke for boxes; focus entity as a c-1 line.",
              "Labels for muted marks use c-muted-dark (#5F6773). Focus labels use c-1-dark (#1A5A8E)."]:
        story.append(bullet(t))
    story.append(sub("Sequential vs. diverging ramps"))
    for t in ["<b>Sequential</b> — value runs low to high with no meaningful midpoint. Single-hue ramp, darker = higher.",
              "<b>Diverging</b> — data has a real reference midpoint (gains vs. losses, above vs. below baseline). Never use diverging for purely positive scales.",
              "Default diverging pair: c-2 red ↔ c-1 blue."]:
        story.append(bullet(t))
    story.append(PageBreak())

    # ── S3: CHART TYPES ──────────────────────────────────────────────────────
    story += section_header("3", "Chart-type rules and examples")
    story.append(body("Each section below states the rules for one chart type and shows "
        "a sample using Growth Lab tokens. Apply the general rules from Sections 1–2 in all cases."))
    story.append(sp(8))

    # Scatter
    story.append(subaccent("Scatter plot"))
    story += chart_rule_block("Scatter plot", C1D, [
        "Circles only. Fill = main tone (c-N), fill-opacity 0.8. Stroke = dark tone (c-N-dark), stroke-opacity 0.8, 1px.",
        "Pop-up pattern: all backdrop points in c-muted / c-muted-dark at 0.8 opacity. Focus point painted once — excluded from the muted layer.",
        "X-axis: use log scale when encoding GDP per capita or any order-of-magnitude variable.",
        "Direct labels in the dark tone of the series; use repel to avoid overlap.",
    ])
    story += chart_sample(draw_scatter(),
        "Sample — GDP per capita (log) vs. economic complexity. Grey = all countries; blue = Pakistan.")

    # Line
    story.append(subaccent("Line chart"))
    story += chart_rule_block("Line chart", C1D, [
        "Line weight: 2px standard; 2.4px for the highlighted focus series. stroke-linejoin: round.",
        "Solid lines only. Dashed lines reserved for projections or forecasts.",
        "Pop-up: muted lines (c-muted, 2px) for backdrop; focus line (c-1, 2.4px) on top.",
        "Direct end-of-line labels preferred over a legend when 1–4 series are shown. Labels use the dark tone.",
    ])
    story += chart_sample(draw_line(),
        "Sample — exports as % of GDP, 2016–2024. Muted = peer countries; blue = Pakistan.")

    # Bar
    story.append(subaccent("Bar chart (vertical and horizontal)"))
    story += chart_rule_block("Bar chart", C2D, [
        "Fill = main tone, full opacity, no stroke. Bars abut directly.",
        "Pop-up: all bars in c-muted; focus bar in c-1 (or c-2 for lead-finding contrast).",
        "Zero baseline drawn at axis weight (ink-2), not gridline weight.",
        "Value labels use the dark tone of the bar color.",
    ])
    story += chart_sample(draw_bar(),
        "Sample — Pakistan export sectors by share. Blue = textiles (focus); grey = all others.")

    # Stacked bar
    story.append(subaccent("Stacked bar and stacked area"))
    story += chart_rule_block("Stacked bar / area", C3D, [
        "Order categories: largest mean share at the bottom, upward.",
        "Stacked bars: 1px paper-white gap between each segment.",
        "Colors assigned in order: c-1 bottom, c-2 middle, c-3 top.",
        "Two-tone option: main + light of one hue when two categories share a parent concept.",
    ])
    story += chart_sample(draw_stacked_bar(),
        "Sample — export composition 2018–2023. Blue = manufactures, red = agriculture, teal = services.")

    # Treemap
    story.append(subaccent("Treemap"))
    story += chart_rule_block("Treemap", C4D, [
        "Tile fill: main tone, full opacity, no stroke. Tiles abut directly.",
        "Pop-up: focus tile(s) in c-1; all others in c-muted.",
        "Tile label: Inter weight 600. White text on dark/saturated tiles; ink-2 on light or muted-grey tiles.",
        "Omit labels on tiles narrower than ~44px or shorter than ~26px.",
    ])
    story += chart_sample(draw_treemap(),
        "Sample — Pakistan export product space. Blue = key textile products; grey = all others.")

    # Boxplot
    story.append(subaccent("Boxplot and violin"))
    story += chart_rule_block("Boxplot / violin", C1D, [
        "Background distribution boxes: c-muted-light fill + c-muted stroke, 1px. Median line: c-muted-dark, 1.5px.",
        "Focus entity (single country, cohort): c-1 line at 2.4px on top of the boxes.",
        "Focus points: fill=c-1, stroke=c-1-dark, both at 0.8 opacity, radius 5px.",
        "Whiskers mark the 10th–90th percentile range, with small end-caps.",
        "End-labels: focus entity → c-1-dark; peer median label → c-muted-dark.",
    ])
    story += chart_sample(draw_boxplot(),
        "Sample — regional GDP per capita distribution by year. Boxes = peer range; blue line = Pakistan.")

    # Radar
    story.append(subaccent("Radar chart"))
    story += chart_rule_block("Radar chart", C4D, [
        "Use to profile one entity across 4–8 normalized dimensions.",
        "Series fill: c-1 at fill-opacity 0.25 so gridlines and labels read through.",
        "Series stroke: c-1, full opacity, 2px, stroke-linejoin round. Vertex dots at 3px, filled c-1.",
        "Second comparison series: c-muted at 0.18 fill opacity, drawn under the focus series.",
    ])
    story += chart_sample(draw_radar(),
        "Sample — country capability profile. Blue = Pakistan; grey = peer average.")

    # Choropleth
    story.append(subaccent("Choropleth map"))
    story += chart_rule_block("Choropleth map", C3D, [
        "Sequential choropleth: single-hue ramp, darker = higher value. Full opacity; 0.5px stroke between regions.",
        "Diverging choropleth: meaningful midpoint only. Red tail = negative, blue = positive.",
        "Never use a rainbow palette — it introduces false boundaries and misleads colour-blind readers.",
        "Include a legend bar with labeled endpoints and midpoint. Source line required below the map.",
    ])
    story += chart_sample(draw_choropleth(),
        "Sample — economic complexity index, South Asia. Tile grid encodes sequential blue ramp.")

    story.append(sp(8))
    story.append(rule_line(RULE))
    story.append(sp(4))
    story.append(Paragraph(
        "Growth Lab, Harvard Kennedy School  ·  growth.lab  ·  June 2026",
        ParagraphStyle("foot",fontName="Helvetica",fontSize=8,textColor=INK4,alignment=TA_CENTER)))

    doc.build(story, onFirstPage=on_cover_page, onLaterPages=on_page)
    print(f"Written: {OUT}")


if __name__ == "__main__":
    build()
