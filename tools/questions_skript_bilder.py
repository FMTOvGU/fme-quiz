# -*- coding: utf-8 -*-
"""Bildfragen mit Abbildungen aus dem Vorlesungsskript FME (mit Quellenangabe)."""
import json, sys, os
sys.path.insert(0, os.path.dirname(__file__))
import questions_bearings_gears as base
from questions_bearings_gears import G, O, de, en

G.update({
    "hypoid": ("Hypoidgetriebe", "hypoid gearbox"),
    "nadelhuelse": ("Nadelhülse", "drawn cup needle roller bearing"),
    "nadelkranz": ("Nadelkranz", "needle roller and cage assembly"),
    "skl2": ("zweireihiges Schrägkugellager", "double-row angular contact ball bearing"),
    "gewaltbruch": ("Gewaltbruch", "forced breakage"),
    "dauerbruch": ("Dauerbruch (Ermüdungsbruch)", "fatigue breakage"),
})

Q = []
SK = "Skript FME, Folie"


def add(topic, image, source, pde, pen, opts, correct, xde, xen):
    Q.append(dict(topic_id=topic, qtype="img", prompt_de=de(pde), prompt_en=en(pen), image=f"img/{image}.jpg",
                  image_source=source, options=opts, correct=correct, explanation_de=de(xde), explanation_en=en(xen)))


B, Z = "bearings", "gears"
SCH, SKF = "Schaeffler (www.schaeffler.de)", "SKF (www.skf.com)"
WB = ("Welches Lager ist abgebildet?", "Which bearing is shown?")


def lager(img, src, folie, opts, correct, xde, xen):
    add(B, img, f"{src} · {SK} {folie}", WB[0], WB[1], [O(f"[{k}]") for k in opts], correct, xde, xen)


lager("foto_rillenkugellager", SCH, 17, ["rkl", "skl", "vpl", "pkl"], 0,
      "[rkl]: eine Kugelreihe in tiefen Laufrillen beider Ringe, symmetrische Schultern.",
      "[rkl]: one row of balls in deep raceway grooves in both rings, symmetrical shoulders.")
lager("foto_schraegkugellager", SCH, 19, ["rkl", "skl", "krl", "arkl"], 1,
      "[skl]: Am Außenring ist eine Schulter deutlich niedriger, die Kugeln laufen schräg. Es trägt Axialkraft nur in einer Richtung.",
      "[skl]: one shoulder of the outer ring is clearly lower and the balls run at an angle. It carries axial force in one direction only.")
lager("foto_schraegkugellager_2reihig", SKF, 19, ["pkl", "skl2", "prl", "rkl"], 1,
      "[skl2]: entspricht zwei Schrägkugellagern in O-Anordnung. Es ist radial und axial hoch belastbar, z. B. bei Getriebewellen.",
      "[skl2]: corresponds to two angular contact ball bearings in O arrangement. It takes high radial and axial loads, e.g. on gear shafts.")
lager("foto_pendelkugellager", SKF, 20, ["skl2", "pkl", "prl", "rkl"], 1,
      "[pkl]: zwei Kugelreihen und eine kugelige Außenringlaufbahn. Der Innenring kann bis ca. 4° kippen.",
      "[pkl]: two rows of balls and a spherical outer ring raceway. The inner ring can tilt by up to approx. 4°.")
lager("foto_vierpunktlager", SKF, 20, ["vpl", "rkl", "skl", "pkl"], 0,
      "[vpl]: geteilter Innenring, Laufbahnen aus zwei Kreisbögen, die Kugel berührt in vier Punkten. Es trägt höhere Axiallast als ein Rillenkugellager.",
      "[vpl]: split inner ring and raceways made of two circular arcs; the ball touches at four points. It carries more axial load than a deep groove ball bearing.")
lager("foto_zylinderrollenlager", SKF, 21, ["nl", "krl", "zrl", "tl"], 2,
      "[zrl]: zylindrische Rollen mit [linienber]. Es ist radial hoch belastbar, aber empfindlich gegen [fluchtf].",
      "[zrl]: cylindrical rollers with [linienber]. It takes high radial loads but is sensitive to [fluchtf].")
lager("foto_nadellager", SCH, 22, ["zrl", "nl", "nadelhuelse", "krl"], 1,
      "[nl]: viele dünne, lange Rollen und eine sehr geringe Bauhöhe. Es nimmt nur Radialkraft auf.",
      "[nl]: many thin, long rollers and a very low section height. It carries radial force only.")
lager("foto_nadelhuelse", SCH, 22, ["nadelkranz", "nadelhuelse", "nl", "zrl"], 1,
      "[nadelhuelse] (DIN 618): dünnwandiger, gezogener Außenring und kein Innenring. Die Welle dient als Laufbahn und muss gehärtet sein (58–65 HRC).",
      "[nadelhuelse] (DIN 618): thin-walled drawn outer cup and no inner ring. The shaft acts as the raceway and must be hardened (58–65 HRC).")
lager("foto_nadelkranz", SCH, 22, ["nadelkranz", "nadelhuelse", "nl", "zrl"], 0,
      "[nadelkranz] (DIN 5405): nur Käfig und Nadeln, ohne Innen- und Außenring. Welle und Bohrung müssen als gehärtete Laufbahnen ausgeführt sein.",
      "[nadelkranz] (DIN 5405): only cage and needles, no inner or outer ring. Shaft and bore must be designed as hardened raceways.")
lager("foto_tonnenlager", SCH, 23, ["tl", "prl", "zrl", "pkl"], 0,
      "[tl]: eine Reihe tonnenförmiger Rollen und eine hohlkugelige Außenringlaufbahn. Es trägt hohe, stoßartige Radiallasten, axial aber nur wenig.",
      "[tl]: one row of barrel-shaped rollers and a hollow-spherical outer ring raceway. It takes high shock-type radial loads but only little axial load.")
lager("foto_pendelrollenlager", SCH, 23, ["tl", "prl", "pkl", "krl"], 1,
      "[prl]: zwei Reihen Tonnenrollen. Es ist radial und axial hoch belastbar, z. B. für Seilrollen und Schiffswellen.",
      "[prl]: two rows of barrel rollers. It takes high radial and axial loads, e.g. for rope sheaves and ship shafts.")
lager("foto_kegelrollenlager", SKF, 24, ["zrl", "krl", "skl", "tl"], 1,
      "[krl]: kegelige Rollen und ein abnehmbarer Außenring. Es wird paarweise in O- oder X-Anordnung eingebaut, z. B. in Radnaben.",
      "[krl]: tapered rollers and a removable outer ring. It is mounted in pairs in O or X arrangement, e.g. in wheel hubs.")
lager("foto_axialrillenkugellager", SKF, 26, ["rkl", "arkl", "azrl", "vpl"], 1,
      "[arkl]: Wellen- und Gehäusescheibe mit Kugelkranz dazwischen. Es ist axial hoch belastbar, aber kaum radial.",
      "[arkl]: shaft and housing washer with a ball and cage assembly between them. It takes high axial loads but hardly any radial load.")
lager("foto_axialzylinderrollenlager", SKF, 26, ["arkl", "azrl", "nadelkranz", "zrl"], 1,
      "[azrl]: flache Scheiben, sternförmig angeordnete Zylinderrollen. Es ist axial sehr hoch belastbar, nimmt aber keine Radiallast auf.",
      "[azrl]: flat washers with cylindrical rollers arranged in a star pattern. It takes very high axial loads but no radial load.")

add(B, "foto_gleitlager", f"www.shop.reiff-tp.de · {SK} 6",
    "Um welche Lagerart handelt es sich?", "What type of bearing is this?",
    [O("[gleitl]", "[gleitl^]"), O("[waelzl]", "[waelzl^]"), O("[nl]", "[nl^]"), O("[dichtung]", "[dichtung^]")], 0,
    "Eine Gleitlagerbuchse: Zwei Flächen gleiten aufeinander, es gibt keine Wälzkörper. Sie ist einfach und klein, dämpft gut und läuft leise.",
    "A plain bearing bush: two surfaces slide on each other and there are no rolling elements. It is simple, compact, damps well and runs quietly.")
add(B, "foto_deckscheibe", f"{SKF} · {SK} 17",
    "Womit ist dieses [rkl] seitlich abgedichtet?", "How is this [rkl] protected at the side?",
    [O("[deckscheibe] (Z)", "[deckscheibe^] (Z)"), O("Berührende [dichtung] (RS)", "Contact [dichtung] (RS)"), O("Gar nicht (offenes Lager)", "Not at all (open bearing)"), O("[kaefig]", "[kaefig^]")], 0,
    "Eine metallische [deckscheibe] (Z) bildet einen Spalt. Sie hält Schmutz ab, berührt den Innenring aber nicht.",
    "A metal [deckscheibe] (Z) forms a gap. It keeps dirt out but does not touch the inner ring.")
add(B, "foto_dichtung", f"{SKF} · {SK} 17",
    "Womit ist dieses [rkl] seitlich abgedichtet?", "How is this [rkl] protected at the side?",
    [O("[deckscheibe] (Z)", "[deckscheibe^] (Z)"), O("Berührende [dichtung] (RS)", "Contact [dichtung] (RS)"), O("Gar nicht (offenes Lager)", "Not at all (open bearing)"), O("[kaefig]", "[kaefig^]")], 1,
    "Eine schwarze Elastomer-[dichtung] (RS) liegt am Innenring an. Sie hält das Fett im Lager; solche Lager sind meist auf Lebensdauer geschmiert.",
    "A black elastomer [dichtung] (RS) touches the inner ring. It keeps the grease in; such bearings are usually lubricated for life.")

SCHL = "Schlecht, Maschinenelemente 2"
FUNK = [O("[festl]", "[festl^]"), O("[losl]", "[losl^]"), O("[stuetzl]", "[stuetzl^]")]
for img, c, xde, xen in (
    ("skizze_loslager", 1, "[losl]: keine axialen Anschläge, nur Radialkräfte. Die Welle kann sich bei Wärmedehnung axial verschieben.",
     "[losl^]: no axial stops, radial forces only. The shaft can move axially when it expands thermally."),
    ("skizze_festlager", 0, "[festl]: Anschläge auf beiden Seiten. Es nimmt Axialkräfte aus beiden Richtungen und Radialkräfte auf.",
     "[festl^]: stops on both sides. It takes axial forces from both directions plus radial forces."),
    ("skizze_stuetzlager", 2, "[stuetzl]: Anschlag nur auf einer Seite. Es nimmt Axialkräfte aus einer Richtung und Radialkräfte auf.",
     "[stuetzl^]: stop on one side only. It takes axial forces from one direction plus radial forces.")):
    add(B, img, f"{SCHL} · {SK} 8", "Welche Lagerfunktion zeigt die Skizze?", "Which bearing function does the sketch show?",
        FUNK, c, xde, xen)

# ---- Getriebe
GO = [O("[stirnrad]", "External [stirnrad]"), O("Innen-Stirnradgetriebe ([hohlrad])", "Internal spur gearbox ([hohlrad])"),
      O("[kegelrad]"), O("[hypoid]"), O("[schnecke]")]
for img, c, xde, xen in (
    ("foto_getriebe_stirnrad", 0, "Außen-[stirnrad]: parallele Achsen, die Räder drehen gegensinnig.", "External [stirnrad]: parallel axes, the gears rotate in opposite directions."),
    ("foto_getriebe_hohlrad", 1, "Innen-Stirnradgetriebe: Ritzel im [hohlrad], parallele Achsen, gleiche Drehrichtung.", "Internal spur gearbox: pinion inside an [hohlrad], parallel axes, same direction of rotation."),
    ("foto_getriebe_kegelrad", 2, "[kegelrad]: kegelförmige Räder, sich schneidende Achsen (meist 90°).", "[kegelrad^]: conical gears with intersecting axes (usually 90°)."),
    ("foto_getriebe_hypoid", 3, "[hypoid]: Kegelrad-ähnlich, aber die Achsen sind versetzt und kreuzen sich, ohne sich zu schneiden.", "[hypoid^]: similar to a bevel gear, but the axes are offset and cross without intersecting."),
    ("foto_getriebe_schnecke", 4, "[schnecke]: Schnecke und Schneckenrad mit gekreuzten Achsen; große Übersetzung in einer Stufe.", "[schnecke^]: worm and worm wheel with crossed axes; large ratio in one stage.")):
    add(Z, img, f"{SCHL} · {SK} 19", "Welche Getriebeart ist abgebildet?", "Which type of gearbox is shown?", GO, c, xde, xen)

VO = [O("[gerade]"), O("[schraeg]"), O("[doppel]"), O("[pfeil]")]
for img, c, xde, xen in (
    ("foto_verz_gerade", 0, "[gerade]: Zähne parallel zur Achse. Sie ist robust und einfach, läuft aber lauter.", "[gerade^]: teeth parallel to the axis. It is robust and simple, but noisier."),
    ("foto_verz_schraeg", 1, "[schraeg]: schräge Zähne, ruhiger Lauf, höhere Überdeckung, aber eine [axialkraft].", "[schraeg^]: inclined teeth, smoother running, higher contact ratio, but an [axialkraft]."),
    ("foto_verz_doppelschraeg", 2, "[doppel]: zwei gegensinnige Schrägverzahnungen mit Nut dazwischen; die Axialkräfte heben sich auf.", "[doppel^]: two opposite helical rows with a groove in between; the axial forces cancel out."),
    ("foto_verz_pfeil", 3, "[pfeil]: zwei gegensinnige Schrägverzahnungen ohne Nut; die Axialkräfte heben sich auf.", "[pfeil^]: two opposite helical rows without a groove; the axial forces cancel out.")):
    add(Z, img, f"{SCHL} · {SK} 64", "Welche Verzahnung haben diese Stirnräder?", "Which gearing do these spur gears have?", VO, c, xde, xen)

SO = [O("[gruebchen]", "[gruebchen^]"), O("[dauerbruch]", "[dauerbruch^]"), O("[gewaltbruch]", "[gewaltbruch^]"),
      O("[fressen]", "[fressen^]"), O("[grauf]", "[grauf^]")]
FZG = "TU München, FZG"
for img, src, folie, c, xde, xen in (
    ("foto_schaden_gruebchen", "Quelle im Skript nicht angegeben", 70, 0,
     "[gruebchen]: kleine muschelförmige Ausbrüche auf der Flanke, entstanden durch Ermüdung infolge hoher Pressung.",
     "[gruebchen^]: small shell-shaped break-outs on the flank, caused by fatigue under high contact pressure."),
    ("foto_schaden_ermuedungsbruch", "Quelle im Skript nicht angegeben", 70, 1,
     "[dauerbruch]: Der Riss wächst langsam vom [zahnfuss] aus; typisch ist die glatte Ermüdungsfläche mit Restgewaltbruch.",
     "[dauerbruch^]: the crack grows slowly from the [zahnfuss]; typical is the smooth fatigue surface with a final forced fracture."),
    ("foto_schaden_gewaltbruch", "Quelle im Skript nicht angegeben", 70, 2,
     "[gewaltbruch]: Der Zahn bricht durch Überlast (z. B. Unfall, Blockieren). Die Bruchfläche ist zerklüftet. Dieser Fall ist nicht durch die Normen abgedeckt.",
     "[gewaltbruch^]: the tooth breaks due to overload (e.g. accident, jamming). The fracture surface is rough. This case is not covered by the standards."),
    ("foto_schaden_fressen", FZG, 71, 3,
     "[fressen]: Riefen in Gleitrichtung durch kurzzeitiges Verschweißen und Aufreißen der Flanken, weil der Schmierfilm thermisch versagt.",
     "[fressen^]: scores in the sliding direction from flanks briefly welding and tearing apart, because the lubricant film fails thermally."),
    ("foto_schaden_graufleckigkeit", FZG, 71, 4,
     "[grauf]: matte, grau schimmernde Flächen durch Mikroermüdung an den Rauheitsspitzen. Sie kann Grübchen begünstigen.",
     "[grauf^]: matt, grey shaded areas from micro-fatigue at the roughness peaks. It can promote pitting.")):
    add(Z, img, f"{src} · {SK} {folie}", "Welcher Zahnradschaden ist abgebildet?", "Which gear failure is shown?", SO, c, xde, xen)

if __name__ == "__main__":
    json.dump(Q, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(Q), "Bildfragen aus dem Skript")
