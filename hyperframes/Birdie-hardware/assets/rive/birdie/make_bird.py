import math, sys
OUT = sys.argv[1]
_id = [100]
def nid():
    _id[0] += 1
    return f"0:{_id[0]}"
def col(h): return "FF" + h.upper()
def ang(dx, dy): return math.atan2(dy, dx)
def path_xml(start, segs, closed=True):
    pts = [start]; outs = [None]; ins = [None]
    for s in segs:
        p0 = pts[-1]
        if s[0] == 'L':
            pts.append(s[1]); ins.append(None); outs.append(None)
        else:
            c, p = s[1], s[2]
            c1 = (p0[0] + 2/3*(c[0]-p0[0]), p0[1] + 2/3*(c[1]-p0[1]))
            c2 = (p[0] + 2/3*(c[0]-p[0]), p[1] + 2/3*(c[1]-p[1]))
            outs[-1] = c1; pts.append(p); ins.append(c2); outs.append(None)
    if closed and abs(pts[-1][0]-pts[0][0]) < 1e-6 and abs(pts[-1][1]-pts[0][1]) < 1e-6:
        ins[0] = ins[-1]; pts.pop(); ins.pop(); outs.pop()
    v = []
    for p, i, o in zip(pts, ins, outs):
        def h(q):
            if q is None: return 0.0, 0.0
            return ang(q[0]-p[0], q[1]-p[1]), math.hypot(q[0]-p[0], q[1]-p[1])
        ir, idist = h(i); orr, od = h(o)
        if idist == 0 and od == 0:
            v.append(f'<StraightVertex x="{p[0]:.3f}" y="{p[1]:.3f}"/>')
        else:
            if idist == 0: ir = orr + math.pi
            if od == 0: orr = ir + math.pi
            v.append(f'<CubicDetachedVertex x="{p[0]:.3f}" y="{p[1]:.3f}" inRotation="{ir:.5f}" inDistance="{idist:.3f}" outRotation="{orr:.5f}" outDistance="{od:.3f}"/>')
    return f'<PointsPath isClosed="{"true" if closed else "false"}" name="Path">' + "".join(v) + '</PointsPath>'
def fill(c): return f'<Fill name="Fill"><SolidColor colorValue="{col(c)}" name="C"/></Fill>'
def stroke(c, w): return f'<Stroke thickness="{w}" cap="1" join="1" name="Stroke"><SolidColor colorValue="{col(c)}" name="C"/></Stroke>'
def shp(name, start, segs, c, closed=True, w=None):
    return f'<Shape name="{name}">' + path_xml(start, segs, closed) + (stroke(c, w) if w else fill(c)) + '</Shape>'
def ellipse(name, cx, cy, w, h, c):
    return f'<Shape x="{cx:.3f}" y="{cy:.3f}" name="{name}"><Ellipse width="{w}" height="{h}" name="Path"/>' + fill(c) + '</Shape>'

# reference illustration coords (1024px, bird facing left) -> feet-local, mirrored to face right
S = 0.14
def R(x, y): return (-(x - 400) * S, (y - 880) * S)
def rel(p, o): return (p[0]-o[0], p[1]-o[1])
def mk(o): return lambda x, y: rel(R(x, y), o)
def P(fn, start, segs):
    st = fn(*start); out = []
    for s in segs:
        out.append(('L', fn(*s[1])) if s[0] == 'L' else ('Q', fn(*s[1]), fn(*s[2])))
    return st, out

PALE="F7D2C7"; SHADE="F2A690"; WING1="EF8B6C"; WING2="EA6F50"; FAR="D9654A"; LINE="C9583F"; CREST="EA7357"; DARK="2A0E09"; SPECK="EE8E72"; LEAF="A9BF8E"; TWIG="8A3B2E"

BODY_O = (0, -11); HEAD_O = R(262, 318); WING_O = R(380, 330); FARW_O = R(360, 305); TAIL_O = R(620, 760); EYE_O = R(255, 315)
LEGS_O = R(428, 762)
TWIG_O = (-107, 8); FEA1_O = (-4, -40); FEA2_O = (14, -46)
ids = {k: nid() for k in ["stage","flyer","body","head","wing","farwing","tail","eye","legs","twig","streaks","fea1","fea2",
                          "aFly","aIdle","aOff","sm","layer","sFly","sIdle","sOff","trig","art","style"]}
def inBody(o): return rel(o, BODY_O)

WING_UP = [('Q',(500,250),(640,360)), ('Q',(800,480),(870,640)), ('Q',(760,640),(700,600)), ('Q',(560,600),(470,560)), ('Q',(360,480),(360,330))]
WING_LO = [('Q',(600,600),(780,640)), ('Q',(880,690),(935,725)), ('Q',(860,745),(800,735)), ('Q',(820,760),(740,752)), ('Q',(640,735),(560,690)), ('Q',(450,620),(430,500))]
w = mk(WING_O)
wing = (
  "".join(shp(f"WingLine{i}", *P(w, a, [('Q', c, b)]), LINE, closed=False, w=1.6) for i, (a, c, b) in enumerate([
      ((450,330),(520,390),(610,500)), ((420,390),(470,470),(560,570)), ((530,320),(610,380),(700,480)),
      ((600,420),(680,480),(760,580)), ((480,470),(540,560),(640,630)) ]))
  + shp("WingUpper", *P(w, (360,330), WING_UP), WING1)
  + shp("WingLower", *P(w, (430,500), WING_LO), WING2))
# far-side wing: same feather shape, darker, sits behind the body and peeks out on the upstroke
fw = mk(WING_O)
farwing = (shp("FarUpper", *P(fw, (360,330), WING_UP), FAR) + shp("FarLower", *P(fw, (430,500), WING_LO), "C9573F"))
h = mk(HEAD_O); e = mk(EYE_O)
eo = rel(EYE_O, HEAD_O)
head = (
  f'<Node x="{eo[0]:.3f}" y="{eo[1]:.3f}" name="Eye" id="{ids["eye"]}">'
  + ellipse("Shine", *e(247,307), 2.6, 2.6, "FFFFFF") + ellipse("Pupil", *e(255,315), 7.4, 7.4, DARK) + '</Node>'
  + shp("Beak", *P(h, (178,318), [('L',(60,356)), ('L',(186,346)), ('L',(178,318))]), DARK)
  + "".join(shp(f"CrestLine{i}", *P(h, a, [('Q', c, b)]), LINE, closed=False, w=1.3) for i, (a, c, b) in enumerate([
      ((175,270),(195,200),(240,150)), ((210,280),(240,210),(290,150)), ((250,275),(280,230),(320,190))]))
  + shp("Crest", *P(h, (160,305), [('Q',(120,210),(205,125)), ('Q',(225,170),(228,190)), ('Q',(245,110),(292,92)),
                                    ('Q',(305,145),(292,168)), ('Q',(318,125),(342,122)), ('Q',(345,175),(318,205)),
                                    ('Q',(338,195),(350,205)), ('Q',(310,270),(245,300)), ('Q',(200,320),(160,305))]), CREST))
b = mk(BODY_O)
speckles = "".join(shp(f"Speck{i}", *P(b, (x, y), [('Q', (x-9, y+12), (x-3, y+26))]), SPECK, closed=False, w=1.6)
                   for i, (x, y) in enumerate([(170,440),(228,420),(200,495),(248,515),(285,462),(232,565),(300,560),(345,585),(218,610),(300,640)]))
shade = shp("HeadShade", *P(b, (245,232), [('Q',(320,152),(440,190)), ('Q',(545,232),(600,335)), ('Q',(470,272),(245,232))]), SHADE)
body = shp("BodyShape", *P(b, (310,165), [('Q',(470,150),(560,300)), ('Q',(700,480),(660,700)), ('Q',(600,812),(400,806)),
                                           ('Q',(200,790),(150,560)), ('Q',(110,330),(220,220)), ('Q',(260,170),(310,165))]), PALE)
t = mk(TAIL_O)
tail = shp("Tail", *P(t, (590,690), [('Q',(800,760),(1016,778)), ('L',(1020,806)), ('Q',(800,814),(600,798)), ('L',(590,690))]), PALE)
# legs hang from the hip so they can fold up and tuck back in flight
lg = mk(LEGS_O)
legs = (f'<Node x="{LEGS_O[0]:.3f}" y="{LEGS_O[1]:.3f}" name="Legs" id="{ids["legs"]}">'
  + shp("LegL", *P(lg, (365,770), [('L',(338,880))]), DARK, closed=False, w=2.4)
  + shp("ToesL", *P(lg, (292,894), [('Q',(320,872),(338,880)), ('Q',(355,884),(372,890))]), DARK, closed=False, w=2.2)
  + shp("LegR", *P(lg, (490,755), [('L',(448,888))]), DARK, closed=False, w=2.4)
  + shp("ToesR", *P(lg, (402,904), [('Q',(430,882),(448,888)), ('Q',(465,892),(478,900))]), DARK, closed=False, w=2.2) + '</Node>')
def bone(name, key, o, inner):
    bo = inBody(o)
    return f'<RootBone x="{bo[0]:.3f}" y="{bo[1]:.3f}" length="1" name="{name}" id="{ids[key]}">{inner}</RootBone>'
farbo = inBody(FARW_O)
flyer = (f'<Node name="Flyer" id="{ids["flyer"]}">'
  + f'<RootBone x="{BODY_O[0]}" y="{BODY_O[1]}" length="1" name="Body" id="{ids["body"]}">'
  + bone("WingBone", "wing", WING_O, wing) + bone("HeadBone", "head", HEAD_O, head)
  + speckles + shade + body + bone("TailBone", "tail", TAIL_O, tail)
  + f'<RootBone x="{farbo[0]:.3f}" y="{farbo[1]:.3f}" length="1" scaleX="0.9" scaleY="0.9" name="FarWingBone" id="{ids["farwing"]}">{farwing}</RootBone>'
  + '</RootBone>' + legs + '</Node>')
def F0(x, y): return (x - 81, y - 124)
tw = lambda x, y: rel(F0(x, y), TWIG_O)
twig = (f'<Node x="{TWIG_O[0]}" y="{TWIG_O[1]}" name="Twig" id="{ids["twig"]}">'
  + shp("LeafR", *P(tw, (150,115), [('Q',(162,96),(182,98)), ('Q',(170,116),(150,115))]), LEAF)
  + shp("LeafL", *P(tw, (2,129), [('Q',(-6,110),(-22,108)), ('Q',(-14,128),(2,129))]), LEAF)
  + shp("Branch", *P(tw, (-26,132), [('Q',(60,122),(186,112))]), TWIG, closed=False, w=4) + '</Node>')
streaks = (f'<Node name="Streaks" id="{ids["streaks"]}" opacity="0">'
  + shp("S1", *P(F0, (30,70), [('L',(-10,92))]), WING1, closed=False, w=4)
  + shp("S2", *P(F0, (40,52), [('L',(6,70))]), WING1, closed=False, w=4)
  + shp("S3", *P(F0, (54,96), [('L',(22,112))]), WING1, closed=False, w=4) + '</Node>')
feathers = (f'<Node x="{FEA1_O[0]}" y="{FEA1_O[1]}" opacity="0" name="Feather1" id="{ids["fea1"]}">'
  + shp("F1", (-9, 4), [('Q',(-1,-8),(9,-4)), ('Q',(1,8),(-9,4))], WING2) + '</Node>'
  + f'<Node x="{FEA2_O[0]}" y="{FEA2_O[1]}" opacity="0" name="Feather2" id="{ids["fea2"]}">'
  + shp("F2", (-7, 3), [('Q',(-1,-7),(7,-3)), ('Q',(1,7),(-7,3))], SHADE) + '</Node>')

EASE = {"out": (0,0,.58,1), "in": (.42,0,1,1), "inout": (.42,0,.58,1), "p2out": (.25,.46,.45,.94),
        "p3in": (.55,.055,.675,.19), "arc": (.3,0,.7,.6), "snap": (.6,0,.4,1)}
BY = BODY_O[1]
CH = {
 "fx": ("flyer",13,0), "fy": ("flyer",14,0), "fr": ("flyer",15,0), "fsx": ("flyer",16,1), "fsy": ("flyer",17,1), "fo": ("flyer",18,1),
 "br": ("body",15,0), "bsx": ("body",16,1), "bsy": ("body",17,1), "by": ("body",91,BY),
 "hr": ("head",15,0), "wr": ("wing",15,0), "wsy": ("wing",17,1), "xr": ("farwing",15,0), "xsy": ("farwing",17,0.9),
 "tr": ("tail",15,0), "ey": ("eye",17,1), "lr": ("legs",15,0), "lsy": ("legs",17,1),
 "twr": ("twig",15,0), "so": ("streaks",18,0), "sx": ("streaks",13,0),
 "f1o": ("fea1",18,0), "f1x": ("fea1",13,FEA1_O[0]), "f1y": ("fea1",14,FEA1_O[1]), "f1r": ("fea1",15,0),
 "f2o": ("fea2",18,0), "f2x": ("fea2",13,FEA2_O[0]), "f2y": ("fea2",14,FEA2_O[1]), "f2r": ("fea2",15,0),
}
def kf(frame, value, ease):
    if ease in ("hold", "linear"):
        return f'<KeyFrameDouble frame="{frame}" value="{value:.5f}" interpolationType="{ease}"/>'
    x1,y1,x2,y2 = EASE[ease]
    return (f'<KeyFrameDouble frame="{frame}" value="{value:.5f}" interpolationType="cubic">'
            f'<CubicEaseInterpolator x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/></KeyFrameDouble>')
def anim(name, aid, dur, loop, tracks):
    byobj = {}
    for ch, (obj, key, dflt) in CH.items():
        keys = sorted(tracks.get(ch) or [(0, dflt, "hold")], key=lambda k: k[0])
        fr = [k[0] for k in keys]; assert len(fr) == len(set(fr)), (name, ch, fr)
        byobj.setdefault(obj, []).append((key, keys))
    body = ""
    for obj, props in byobj.items():
        body += f'<KeyedObject objectId="{ids[obj]}">' + "".join(
            f'<KeyedProperty propertyKey="{key}">' + "".join(kf(*k) for k in keys) + '</KeyedProperty>' for key, keys in props) + '</KeyedObject>'
    return f'<LinearAnimation loopValue="{loop}" fps="60" duration="{dur}" name="{name}" id="{ids[aid]}">{body}</LinearAnimation>'

# One wingbeat = upstroke (wing raised and spread) then a quicker downstroke (swept down, foreshortened).
UP, DOWN = 1.05, -0.45
def beats(start, n, up=5, down=4, end_rest=True, fold=0.0, include_first=True):
    tr = {"wr": [], "wsy": [], "xr": [], "xsy": [], "by": []}
    f = start
    for i in range(n):
        if i or include_first:
            tr["wr"].append((f, DOWN if i else fold, "inout")); tr["wsy"].append((f, 0.62 if i else 1, "inout"))
            tr["xr"].append((f, DOWN+0.1 if i else fold, "inout")); tr["xsy"].append((f, 0.55 if i else 0.9, "inout"))
            tr["by"].append((f, BY-1.5 if i else BY, "inout"))
        tr["wr"].append((f+up, UP, "snap")); tr["wsy"].append((f+up, 1.12, "snap"))
        tr["xr"].append((f+up, UP+0.15, "snap")); tr["xsy"].append((f+up, 1.0, "snap"))
        tr["by"].append((f+up, BY+1.5, "snap"))
        f += up + down
    if end_rest:
        tr["wr"].append((f, DOWN, "inout")); tr["wsy"].append((f, 0.62, "inout"))
        tr["xr"].append((f, DOWN+0.1, "inout")); tr["xsy"].append((f, 0.55, "inout")); tr["by"].append((f, BY-1.5, "inout"))
    return tr, f
def merge(*ds):
    out = {}
    for d in ds:
        for k, v in d.items(): out.setdefault(k, []).extend(v)
    return out

# ---- FlyIn: beats in with legs tucked, legs reach down, wings brake, lands ----
fb, fend = beats(0, 5, up=4, down=4, end_rest=False)   # frames 0..40
fly = anim("FlyIn", "aFly", 90, "oneShot", merge(fb, {
 "wr": [(40, 1.2, "out"), (47, 0.2, "inout"), (56, -0.05, "inout"), (64, 0, "hold")],
 "wsy": [(40, 1.15, "out"), (47, 1, "inout"), (64, 1, "hold")],
 "xr": [(40, 1.3, "out"), (47, 0.2, "inout"), (64, 0, "hold")],
 "xsy": [(40, 1.0, "out"), (47, 0.9, "inout"), (64, 0.9, "hold")],
 "by": [(40, BY, "inout"), (48, BY, "hold")],
 "fx": [(0,-360,"p2out"), (45,0,"hold")], "fy": [(0,-190,"out"), (45,0,"hold")],
 "fr": [(0,-0.3,"out"), (45,0,"hold")], "fo": [(0,0,"linear"), (8,1,"hold")],
 "lr": [(0,0.9,"hold"), (30,0.9,"out"), (42,-0.1,"inout"), (50,0,"hold")],
 "lsy": [(0,0.3,"hold"), (30,0.3,"out"), (42,1.08,"inout"), (50,1,"hold")],
 "br": [(0,0.1,"hold"), (36,0.1,"inout"), (45,-0.12,"inout"), (60,0,"hold")],
 "bsx": [(45,1,"out"), (51,1.12,"inout"), (60,0.96,"inout"), (68,1.02,"inout"), (78,1,"hold")],
 "bsy": [(45,1,"out"), (51,0.85,"inout"), (60,1.06,"inout"), (68,0.98,"inout"), (78,1,"hold")],
 "hr": [(0,0.06,"hold"), (45,0.06,"inout"), (55,-0.06,"inout"), (70,0,"hold")],
 "tr": [(0,-0.15,"hold"), (40,-0.15,"out"), (47,0.45,"inout"), (58,-0.05,"inout"), (70,0,"hold")],
 "twr": [(45,0,"out"), (52,0.035,"inout"), (60,-0.015,"inout"), (68,0.006,"inout"), (77,0,"hold")],
}))
idle = anim("Idle", "aIdle", 144, "loop", {
 "bsy": [(0,1,"inout"), (24,1.03,"inout"), (48,1,"inout"), (72,1.03,"inout"), (96,1,"inout"), (120,1.03,"inout"), (144,1,"hold")],
 "ey": [(0,1,"hold"), (8,1,"linear"), (11,0.1,"linear"), (14,1,"hold"), (100,1,"linear"), (103,0.1,"linear"), (106,1,"hold")],
 "hr": [(0,0,"hold"), (28,0,"out"), (40,-0.16,"hold"), (70,-0.16,"inout"), (84,0.1,"hold"), (104,0.1,"inout"), (116,0,"hold")],
 "tr": [(0,0,"hold"), (50,0,"out"), (55,0.3,"inout"), (60,0,"out"), (65,0.3,"inout"), (70,0,"hold")],
 "wr": [(0,0,"hold"), (126,0,"inout"), (131,0.22,"inout"), (136,-0.05,"inout"), (141,0,"hold")],
 "xsy": [(0,0.9,"hold")],
})
# ---- TakeOff: crouch, wings lift, legs push off then fold and tuck, strong beats away ----
tb, tend = beats(16, 6, up=4, down=3, include_first=False)  # frames 16..58
off = anim("TakeOff", "aOff", 90, "oneShot", merge(tb, {
 "wr": [(0,0,"inout"), (12,0.5,"out"), (16,0.2,"inout")], "wsy": [(0,1,"inout"), (12,1.05,"out"), (16,0.8,"inout")],
 "xr": [(0,0,"inout"), (12,0.6,"out"), (16,0.3,"inout")], "xsy": [(0,0.9,"inout"), (12,1.0,"out"), (16,0.75,"inout")],
 "by": [(0,BY,"hold"), (16,BY,"inout")],
 "br": [(0,0,"in"), (13,0.18,"out"), (18,-0.28,"inout"), (40,-0.3,"hold")],
 "bsx": [(0,1,"in"), (13,1.1,"out"), (18,0.92,"inout"), (28,1,"hold")],
 "bsy": [(0,1,"in"), (13,0.82,"out"), (18,1.12,"inout"), (28,1,"hold")],
 "lr": [(0,0,"hold"), (13,0,"out"), (17,-0.15,"inout"), (25,0.95,"hold")],
 "lsy": [(0,1,"in"), (13,0.85,"out"), (17,1.15,"inout"), (25,0.3,"hold")],
 "tr": [(0,0,"out"), (13,0.6,"inout"), (20,-0.25,"inout"), (30,0.1,"hold")],
 "hr": [(0,0,"inout"), (12,0.08,"inout"), (20,-0.1,"inout"), (30,-0.05,"hold")],
 "fx": [(0,0,"hold"), (16,0,"p3in"), (52,600,"hold")], "fy": [(0,0,"hold"), (16,0,"arc"), (52,-360,"hold")],
 "fr": [(0,0,"hold"), (16,0,"in"), (43,1.012291,"hold")], "fsx": [(0,1,"hold")],
 "fo": [(0,1,"hold"), (44,1,"linear"), (52,0,"hold")],
 "so": [(0,0,"hold"), (18,0,"linear"), (24,0.9,"out"), (44,0,"hold")], "sx": [(0,0,"hold"), (18,0,"out"), (44,45,"hold")],
 "twr": [(0,0,"hold"), (14,0,"out"), (20,0.04,"inout"), (28,-0.045,"inout"), (36,0.022,"inout"), (44,-0.01,"inout"), (52,0.004,"inout"), (60,0,"hold")],
 "f1o": [(0,0,"hold"), (19,0,"linear"), (28,1,"hold"), (66,1,"linear"), (90,0,"hold")],
 "f1x": [(0,FEA1_O[0],"hold"), (19,FEA1_O[0],"inout"), (90,FEA1_O[0]-24,"hold")],
 "f1y": [(0,FEA1_O[1],"hold"), (19,FEA1_O[1],"inout"), (90,FEA1_O[1]+34,"hold")],
 "f1r": [(0,0,"hold"), (19,0,"inout"), (90,-0.9,"hold")],
 "f2o": [(0,0,"hold"), (24,0,"linear"), (32,1,"hold"), (66,1,"linear"), (90,0,"hold")],
 "f2x": [(0,FEA2_O[0],"hold"), (24,FEA2_O[0],"inout"), (90,FEA2_O[0]+20,"hold")],
 "f2y": [(0,FEA2_O[1],"hold"), (24,FEA2_O[1],"inout"), (90,FEA2_O[1]+32,"hold")],
 "f2r": [(0,0,"hold"), (24,0,"inout"), (90,1.0,"hold")],
}))
sm = (f'<StateMachine name="Bird" id="{ids["sm"]}"><StateMachineTrigger name="takeOff" id="{ids["trig"]}"/>'
  f'<StateMachineLayer name="Life" id="{ids["layer"]}"><AnyState x="0" y="-150"/><ExitState x="600" y="-150"/>'
  f'<EntryState x="0" y="0"><StateTransition stateToId="{ids["sFly"]}"/></EntryState>'
  f'<AnimationState x="200" y="0" animationId="{ids["aFly"]}" id="{ids["sFly"]}"><StateTransition stateToId="{ids["sIdle"]}" enableExitTime="true" exitTimeIsPercetange="true" exitTime="100"/></AnimationState>'
  f'<AnimationState x="400" y="0" animationId="{ids["aIdle"]}" id="{ids["sIdle"]}"><StateTransition stateToId="{ids["sOff"]}" duration="100"><TransitionTriggerCondition inputId="{ids["trig"]}"/></StateTransition></AnimationState>'
  f'<AnimationState x="600" y="0" animationId="{ids["aOff"]}" id="{ids["sOff"]}"/></StateMachineLayer></StateMachine>')
doc = (f'<Rive version="1" kind="fragment"><Artboard defaultStateMachineId="{ids["sm"]}" styleId="{ids["style"]}" width="1920" height="1080" name="Bird" id="{ids["art"]}">'
  f'<LayoutComponentStyle name="Artboard Style" id="{ids["style"]}"/>'
  f'<Node x="961" y="596" scaleX="0.955" scaleY="0.955" name="Stage" id="{ids["stage"]}">'
  + feathers + flyer + streaks + twig + '</Node>' + sm + fly + idle + off + '</Artboard></Rive>')
open(OUT + "/scene.rml", "w").write(doc)
print("ok")
