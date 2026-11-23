# -*- coding: utf-8 -*-
"""Fragen Kapitel 08 (Wälzlager) und 10 (Getriebe/Zahnräder).
Platzhalter [key] werden aus dem Glossar zu {{de|en}} bzw. {{en|de}} ersetzt,
[key^] = englischer Begriff mit großem Anfangsbuchstaben."""

G = {
    # Lager
    "rkl": ("Rillenkugellager", "deep groove ball bearing"),
    "skl": ("Schrägkugellager", "angular contact ball bearing"),
    "pkl": ("Pendelkugellager", "self-aligning ball bearing"),
    "vpl": ("Vierpunktlager", "four-point contact bearing"),
    "zrl": ("Zylinderrollenlager", "cylindrical roller bearing"),
    "krl": ("Kegelrollenlager", "tapered roller bearing"),
    "nl": ("Nadellager", "needle roller bearing"),
    "prl": ("Pendelrollenlager", "spherical roller bearing"),
    "tl": ("Tonnenlager", "barrel bearing"),
    "arkl": ("Axial-Rillenkugellager", "axial deep groove ball bearing"),
    "azrl": ("Axial-Zylinderrollenlager", "axial cylindrical roller bearing"),
    "festl": ("Festlager", "locating bearing"),
    "losl": ("Loslager", "non-locating bearing"),
    "stuetzl": ("Stützlager", "support bearing"),
    "fll": ("Fest-Los-Lagerung", "locating/non-locating bearing arrangement"),
    "schwl": ("schwimmende Lagerung", "floating bearing arrangement"),
    "angl": ("angestellte Lagerung", "adjusted bearing arrangement"),
    "oanord": ("O-Anordnung", "O-arrangement"),
    "xanord": ("X-Anordnung", "X-arrangement"),
    "kaefig": ("Käfig", "cage"),
    "waelzk": ("Wälzkörper", "rolling element"),
    "gleitl": ("Gleitlager", "plain bearing"),
    "waelzl": ("Wälzlager", "rolling bearing"),
    "lagerspiel": ("Lagerluft", "bearing clearance"),
    "lagerluft": ("Lagerluft", "bearing clearance"),
    "bohrkz": ("Bohrungskennzahl", "bore code"),
    "umfangslast": ("Umfangslast", "circumferential load"),
    "punktlast": ("Punktlast", "point load"),
    "passungsrost": ("Passungsrost", "fretting corrosion"),
    "dichtung": ("Dichtung", "seal"),
    "deckscheibe": ("Deckscheibe", "shield"),
    "statkz": ("statische Tragzahl C0", "static load rating C0"),
    "dynkz": ("dynamische Tragzahl C", "dynamic load rating C"),
    "lebexp": ("Lebensdauerexponent", "life exponent"),
    "nomleb": ("nominelle Lebensdauer", "nominal service life"),
    "punktber": ("Punktberührung", "point contact"),
    "linienber": ("Linienberührung", "line contact"),
    "fluchtf": ("Fluchtungsfehler", "misalignment"),
    "druckl": ("Drucklinien", "pressure lines"),
    "stuetzbasis": ("Stützbasis", "support distance"),
    # Getriebe
    "gerade": ("Geradverzahnung", "straight-cut gearing"),
    "schraeg": ("Schrägverzahnung", "helical gearing"),
    "pfeil": ("Pfeilverzahnung", "herringbone gearing"),
    "doppel": ("Doppelschrägverzahnung", "double helical gearing"),
    "stirnrad": ("Stirnradgetriebe", "spur gearbox"),
    "kegelrad": ("Kegelradgetriebe", "bevel gearbox"),
    "schnecke": ("Schneckengetriebe", "worm gearbox"),
    "hohlrad": ("Hohlrad", "internal gear"),
    "zahnstange": ("Zahnstange", "rack"),
    "ritzel": ("Ritzel", "pinion"),
    "eingriffsw": ("Eingriffswinkel", "pressure angle"),
    "modul": ("Modul", "module"),
    "teilkreis": ("Teilkreis", "pitch circle"),
    "grundkreis": ("Grundkreis", "base circle"),
    "ueberdeckung": ("Profilüberdeckung", "contact ratio"),
    "profilv": ("Profilverschiebung", "profile shift"),
    "unterschnitt": ("Unterschnitt", "undercut"),
    "zahnfuss": ("Zahnfuß", "tooth root"),
    "zahnkopf": ("Zahnkopf", "tooth tip"),
    "gruebchen": ("Grübchenbildung", "pitting"),
    "fressen": ("Fressen", "scuffing"),
    "grauf": ("Graufleckigkeit", "micropitting"),
    "zfbruch": ("Zahnfußbruch", "tooth root breakage"),
    "evolvente": ("Evolventenverzahnung", "involute gearing"),
    "zykloide": ("Zykloidenverzahnung", "cycloidal gearing"),
    "uebers": ("Übersetzung", "transmission ratio"),
    "wirkungsgrad": ("Wirkungsgrad", "efficiency"),
    "axialkraft": ("Axialkraft", "axial force"),
    "achsabstand": ("Achsabstand", "center distance"),
    "zahnzahl": ("Zähnezahl", "number of teeth"),
    "tangkraft": ("Tangentialkraft", "tangential force"),
    "flankenlinie": ("Flankenlinie", "flank line"),
}


def de(s):
    import re
    return re.sub(r"\[(\w+)\^?\]", lambda m: "{{%s|%s}}" % G[m.group(1)], s)


def en(s):
    import re
    def rep(m):
        d, e = G[m.group(1)]
        if m.group(2):
            e = e[0].upper() + e[1:]
        return "{{%s|%s}}" % (e, d)
    return re.sub(r"\[(\w+)(\^?)\]", rep, s)


def O(d, e=None):
    """Antwortoption (de, en)."""
    return {"de": de(d), "en": en(e if e is not None else d)}


Q = []


def add(topic, qtype, pde, pen, options=None, correct=None, xde="", xen="", image=None, source=None):
    Q.append(dict(topic_id=topic, qtype=qtype, prompt_de=de(pde), prompt_en=en(pen), image=image,
                  image_source=(source or ("Eigene Darstellung, Lehrstuhl FMT" if image else None)),
                  options=options, correct=correct, explanation_de=de(xde), explanation_en=en(xen)))


B = "bearings"
WHICH = ("Welches Lager ist hier im Schnitt dargestellt?", "Which bearing is shown here in section?")

def img_bearing(file, opts, correct, xde, xen):
    add(B, "img", WHICH[0], WHICH[1], [O(f"[{k}]") for k in opts], correct, xde, xen, image=f"img/{file}")

img_bearing("lager_rillenkugellager.svg", ["skl", "rkl", "pkl", "vpl"], 1,
    "Ein [rkl]: eine Kugelreihe, die in rillenförmigen Laufbahnen beider Ringe läuft. Häufigstes und günstigstes Radiallager.",
    "A [rkl]: one row of balls running in groove-shaped raceways in both rings. The most common and cheapest radial bearing.")
img_bearing("lager_schraegkugellager.svg", ["rkl", "arkl", "skl", "pkl"], 2,
    "Ein [skl]: Die Ringe haben je eine hohe und eine niedrige Schulter, die Kugeln laufen schräg (Druckwinkel α). Es nimmt Axialkraft nur in einer Richtung auf.",
    "An [skl]: each ring has one high and one low shoulder, so the balls run at an angle (contact angle α). It takes axial force in one direction only.")
img_bearing("lager_pendelkugellager.svg", ["pkl", "prl", "rkl", "skl"], 0,
    "Ein [pkl]: zwei Kugelreihen und eine hohlkugelige Laufbahn im Außenring. Dadurch gleicht es [fluchtf] bis ca. 4° aus.",
    "A [pkl]: two rows of balls and a hollow-spherical raceway in the outer ring. This lets it compensate [fluchtf] of up to approx. 4°.")
img_bearing("lager_zylinderrollenlager.svg", ["nl", "krl", "zrl", "tl"], 2,
    "Ein [zrl] (Bauform NU): Die zylindrischen Rollen werden von Borden am Außenring geführt, der Innenring hat keine Borde. So ist es als [losl] einsetzbar.",
    "A [zrl] (design NU): the cylindrical rollers are guided by ribs on the outer ring and the inner ring has no ribs. This makes it usable as a [losl].")
img_bearing("lager_kegelrollenlager.svg", ["zrl", "krl", "skl", "prl"], 1,
    "Ein [krl]: kegelige Rollen und kegelige Laufbahnen; der Außenring ist abnehmbar. Es trägt hohe Radialkräfte und Axialkräfte in einer Richtung und wird meist paarweise in O- oder X-Anordnung eingebaut.",
    "A [krl]: tapered rollers and conical raceways; the outer ring is removable. It carries high radial forces and axial forces in one direction, and is usually mounted in pairs in O or X arrangement.")
img_bearing("lager_nadellager.svg", ["zrl", "nl", "rkl", "azrl"], 1,
    "Ein [nl]: sehr dünne, lange Rollen (Durchmesser ≤ 5 mm, Länge ≥ 2,5 · d). Es ist sehr kompakt, braucht wenig radialen Bauraum und nimmt nur Radialkräfte auf.",
    "A [nl]: very thin, long rollers (diameter ≤ 5 mm, length ≥ 2.5 · d). It is very compact, needs little radial space and carries radial forces only.")
img_bearing("lager_pendelrollenlager.svg", ["pkl", "tl", "prl", "krl"], 2,
    "Ein [prl]: zwei Reihen tonnenförmiger Rollen in einer hohlkugeligen Außenringlaufbahn. Es ist radial und axial hoch belastbar und gleicht Schiefstellungen bis ca. 0,5° aus (bis 2° bei geringer Last).",
    "A [prl]: two rows of barrel-shaped rollers in a hollow-spherical outer ring raceway. It takes high radial and axial loads and compensates misalignment of approx. 0.5° (up to 2° at low load).")
img_bearing("lager_axialrillenkugellager.svg", ["rkl", "skl", "arkl", "azrl"], 2,
    "Ein [arkl]: Die Kugeln laufen zwischen einer Wellenscheibe und einer Gehäusescheibe. Es ist axial hoch belastbar, aber kaum radial.",
    "An [arkl]: the balls run between a shaft washer and a housing washer. It takes high axial loads but hardly any radial load.")

add(B, "img", "Welche Lageranordnung ist dargestellt? (gestrichelt: [druckl])",
    "Which bearing arrangement is shown? (dashed: [druckl])",
    [O("[oanord]"), O("[xanord]"), O("[fll]"), O("[schwl]")], 0,
    "[oanord]: Die [druckl] zeigen nach außen und schneiden die Achse außerhalb der Lager. Das ergibt eine große [stuetzbasis] und eine hohe Kippsteifigkeit.",
    "[oanord^]: the [druckl] point outwards and meet the axis outside the bearings. This gives a large [stuetzbasis] and high tilting stiffness.",
    image="img/lagerung_o.svg")
add(B, "img", "Welche Lageranordnung ist dargestellt? (gestrichelt: [druckl])",
    "Which bearing arrangement is shown? (dashed: [druckl])",
    [O("[oanord]"), O("[xanord]"), O("[fll]"), O("[schwl]")], 1,
    "[xanord]: Die [druckl] zeigen nach innen und schneiden sich zwischen den Lagern. Die [stuetzbasis] ist kleiner, dafür lässt die Anordnung mehr Winkelfehler zu.",
    "[xanord^]: the [druckl] point inwards and cross between the bearings. The [stuetzbasis] is smaller, but the arrangement tolerates more angular error.",
    image="img/lagerung_x.svg")

add(B, "mc", "Welches ist das am häufigsten verwendete und kostengünstigste Radial-Wälzlager?",
    "Which is the most commonly used and most cost-effective radial rolling bearing?",
    [O("[zrl]"), O("[rkl]"), O("[krl]"), O("[nl]")], 1,
    "Das [rkl] ist das universelle Standardlager. Es nimmt Radial- und Axialkräfte in beiden Richtungen auf und eignet sich als [festl].",
    "The [rkl] is the universal standard bearing. It takes radial and axial forces in both directions and is suitable as a [festl].")
add(B, "mc", "Eine lange Welle biegt sich stark durch, die Lagerstellen fluchten nicht. Welches Lager gleicht Schiefstellungen bis ca. 4° aus?",
    "A long shaft deflects considerably and the bearing seats are misaligned. Which bearing compensates misalignment of up to approx. 4°?",
    [O("[pkl]"), O("[zrl]"), O("[krl]"), O("[nl]")], 0,
    "Das [pkl] ist durch die hohlkugelige Außenringlaufbahn winkeleinstellbar. [zrl] und [krl] reagieren dagegen sehr empfindlich auf [fluchtf].",
    "The [pkl] is self-aligning thanks to its hollow-spherical outer ring raceway. [zrl^] and [krl] are very sensitive to [fluchtf].")
add(B, "mc", "Was gibt das Kurzzeichen eines Wälzlagers (z. B. 6205) nach DIN 623 an?",
    "What does the designation of a rolling bearing (e.g. 6205) indicate according to DIN 623?",
    [O("Lagerart, Maßreihe und Bohrungsdurchmesser (codiert)", "Bearing type, dimension series and bore diameter (coded)"),
     O("Hersteller und Herstellungsjahr", "Manufacturer and year of production"),
     O("Zulässige Drehzahl und Lebensdauer", "Permissible speed and service life"),
     O("Werkstoff und Härte der Wälzkörper", "Material and hardness of the rolling elements")], 0,
    "Das Basiszeichen enthält codiert Lagerart, Maßreihe und Bohrungsdurchmesser. Vorsetz- und Nachsetzzeichen kennzeichnen Einzelteile oder Abweichungen vom Standard.",
    "The basic designation contains the bearing type, dimension series and bore diameter in coded form. Prefixes and suffixes identify individual parts or deviations from the standard.")
add(B, "mc", "Was ist ein wesentlicher Vorteil von [waelzl]n gegenüber [gleitl]n?",
    "What is a key advantage of [waelzl]s over [gleitl]s?",
    [O("International genormt und dadurch leicht austauschbar", "Internationally standardized and therefore easily interchangeable"),
     O("Unempfindlich gegen Stöße", "Insensitive to shocks"),
     O("Leiserer Lauf bei hohen Drehzahlen", "Quieter running at high speeds"),
     O("Höhere Grenzdrehzahl", "Higher speed limit")], 0,
    "Wälzlager sind genormte Massenprodukte: Ein Lager mit gleichem Kurzzeichen passt herstellerübergreifend. Außerdem haben sie meist weniger Reibung und brauchen wenig Wartung. Stoßempfindlichkeit, Geräusche und die niedrigere Grenzdrehzahl sind dagegen Nachteile.",
    "Rolling bearings are standardized mass products: a bearing with the same designation fits regardless of manufacturer. They also usually have lower friction and need little maintenance. Sensitivity to shocks, noise and the lower speed limit are disadvantages.")
add(B, "tf", "Ein [losl] nimmt nur Radialkräfte auf.", "A [losl] absorbs radial forces only.", None, True,
    "Richtig. Das [losl] ist axial verschiebbar und gleicht so Wärmedehnungen aus. Die Axialkräfte nimmt allein das [festl] auf.",
    "Correct. The [losl] can move axially to compensate thermal expansion. Axial forces are taken by the [festl] alone.")
add(B, "tf", "[nl] können hohe Axialkräfte aufnehmen.", "[nl^]s can absorb high axial forces.", None, False,
    "Falsch. [nl] nehmen nur Radialkräfte auf. Ihr Vorteil ist der sehr geringe radiale Bauraum bei hoher Steifigkeit.",
    "False. [nl^]s carry radial forces only. Their advantage is very little radial installation space with high stiffness.")
add(B, "mc", "Welchen Wert hat der [lebexp] p für Kugellager?",
    "What is the value of the [lebexp] p for ball bearings?",
    [O("p = 3"), O("p = 10/3"), O("p = 2"), O("p = 1/3")], 0,
    "Kugellager haben [punktber], daher p = 3. Rollenlager haben [linienber], daher p = 10/3. Es gilt L10 = (C/P)^p · 10⁶ Umdrehungen.",
    "Ball bearings have [punktber], so p = 3. Roller bearings have [linienber], so p = 10/3. L10 = (C/P)^p · 10⁶ revolutions.")
add(B, "tf", "Die [nomleb] L10 wird von 90 % einer Gruppe gleicher Lager erreicht oder überschritten.",
    "The [nomleb] L10 is reached or exceeded by 90 % of a group of identical bearings.", None, True,
    "Richtig. L10 entspricht 90 % Erlebenswahrscheinlichkeit, also 10 % Ausfallwahrscheinlichkeit. Lebensdauerangaben sind statistische Aussagen.",
    "Correct. L10 corresponds to 90 % survival probability, i.e. 10 % failure probability. Service life values are statistical statements.")
add(B, "mc", "Was bedeutet das Nachsetzzeichen 2RS bei einem [rkl]?",
    "What does the suffix 2RS mean for a [rkl]?",
    [O("[deckscheibe] auf beiden Seiten", "[deckscheibe^]s on both sides"),
     O("[dichtung]en auf beiden Seiten", "[dichtung^]s on both sides"),
     O("[lagerspiel] größer als normal", "[lagerspiel^] larger than normal"),
     O("Toleranz enger als normal", "Tolerance tighter than normal")], 1,
    "2RS steht für berührende Dichtungen auf beiden Seiten. Z bzw. 2Z bezeichnet Deckscheiben (Spaltabdichtung). Gedichtete Lager sind meist auf Lebensdauer gefettet.",
    "2RS means contact seals on both sides. Z or 2Z denotes shields (gap seal). Sealed bearings are usually greased for life.")
add(B, "mc", "Die [lagerluft] wird im Betrieb durch Wärmedehnung oder einen festen Sitz kleiner. Was kann passieren, wenn sie ganz verschwindet?",
    "In operation the [lagerluft] is reduced by thermal expansion or a tight fit. What can happen if it disappears completely?",
    [O("Das Lager kann klemmen (verspannen)", "The bearing can jam"),
     O("Das Lager läuft dadurch leiser und länger", "The bearing runs quieter and longer"),
     O("Die Wälzkörper fallen heraus", "The rolling elements fall out"),
     O("Nichts – Lagerluft ist nur für die Montage wichtig", "Nothing – clearance only matters for mounting")], 0,
    "Ohne Restluft verspannen sich Ringe und Wälzkörper: Reibung und Temperatur steigen, das Lager kann klemmen. Abhilfe ist eine größere Luftklasse (z. B. C3).",
    "Without remaining clearance the rings and rolling elements are preloaded: friction and temperature rise and the bearing can jam. The remedy is a larger clearance class (e.g. C3).")
add(B, "match", "Ordne jedem Lager die passende Eigenschaft zu.", "Match each bearing to its typical property.",
    {"left": [O("[rkl]"), O("[zrl] NU", "[zrl] NU"), O("[pkl]"), O("[krl]"), O("[nl]")],
     "right": [O("Universallager, radial + axial in beide Richtungen", "Universal bearing, radial + axial in both directions"),
               O("[losl] mit Verschiebung im Lager", "[losl^] with displacement inside the bearing"),
               O("Gleicht große Schiefstellungen aus", "Compensates large misalignment"),
               O("Paarweise in O- oder X-Anordnung", "Mounted in pairs in O or X arrangement"),
               O("Sehr kleiner radialer Bauraum", "Very small radial installation space")]},
    None,
    "Typische Einsatzfälle laut Skript: [rkl] = universell; [zrl] NU = Loslager; [pkl] = Winkelausgleich; [krl] = angestellte Lagerung; [nl] = wenig Bauraum.",
    "Typical uses according to the lecture: [rkl] = universal; [zrl] NU = non-locating bearing; [pkl] = misalignment compensation; [krl] = adjusted arrangement; [nl] = little installation space.")
add(B, "mc", "In einer [fll] soll sich die Welle bei Erwärmung im Loslager selbst verschieben können, ohne Schiebesitz. Welches Lager eignet sich?",
    "In a [fll] the shaft should be able to move inside the non-locating bearing itself when heated, without a sliding fit. Which bearing is suitable?",
    [O("[rkl]"), O("[zrl] NU", "[zrl] NU"), O("[skl]"), O("[arkl]")], 1,
    "Beim [zrl] NU (bordloser Innenring) erfolgt die Verschiebung zwischen Rollen und Laufbahn. Beim [rkl] als Loslager muss dagegen ein Ring in seinem Sitz verschiebbar sein.",
    "In the [zrl] NU (ribless inner ring) the displacement takes place between rollers and raceway. A [rkl] used as non-locating bearing instead needs one ring to slide in its seat.")
add(B, "tf", "Ein Lagerring mit [umfangslast] braucht einen festen Sitz (Presspassung).",
    "A bearing ring subjected to [umfangslast] needs a tight fit (interference fit).", None, True,
    "Richtig. Bei Umfangslast würde ein loser Ring „wandern“ und [passungsrost] verursachen. Bei Punktlast ist ein loser Sitz zulässig.",
    "Correct. Under circumferential load a loose ring would 'creep' and cause [passungsrost]. Under point load a loose fit is permissible.")
add(B, "mc", "Welche Aufgabe hat der [kaefig] im Wälzlager?", "What is the task of the [kaefig] in a rolling bearing?",
    [O("Er überträgt die Radialkraft auf den Außenring", "It transmits the radial force to the outer ring"),
     O("Er führt die [waelzk] und hält sie auf Abstand", "It guides the [waelzk]s and keeps them spaced apart"),
     O("Er dichtet das Lager nach außen ab", "It seals the bearing from the outside"),
     O("Er erhöht die Lagerluft", "It increases the bearing clearance")], 1,
    "Der Käfig führt die Wälzkörper und hält sie auf Abstand. Außerdem speichert und verteilt er Schmierfett und dämpft Schwingungen. Er überträgt keine Lagerkraft.",
    "The cage guides the rolling elements and keeps them spaced apart. It also stores and distributes grease and damps vibrations. It does not transmit bearing loads.")
add(B, "tf", "[waelzl] sind stoßunempfindlicher als hydrodynamische [gleitl].",
    "[waelzl^]s are less sensitive to shocks than hydrodynamic [gleitl]s.", None, False,
    "Falsch. Wälzlager sind stoßempfindlich, besonders im Stillstand und bei niedriger Drehzahl. Hydrodynamische Gleitlager dämpfen gut.",
    "False. Rolling bearings are sensitive to shocks, especially at standstill and low speed. Hydrodynamic plain bearings have good damping.")
add(B, "mc", "Wann wird ein Wälzlager nach der [statkz] ausgelegt?",
    "When is a rolling bearing designed using the [statkz]?",
    [O("Bei hohen Drehzahlen", "At high speeds"),
     O("Im Stillstand, bei n < 10 min⁻¹ oder langsamen Schwenkbewegungen", "At standstill, at n < 10 rpm or slow oscillating motion"),
     O("Nur bei reiner Axiallast", "Only under pure axial load"),
     O("Immer, wenn die Last schwankt", "Whenever the load fluctuates")], 1,
    "Statische Beanspruchung liegt vor, wenn sich das Lager unter Last nicht (oder kaum) dreht. Maßgebend sind dann plastische Eindrückungen. Statisch/dynamisch bezieht sich auf die Drehung, nicht auf den zeitlichen Lastverlauf.",
    "Static stress applies when the bearing does not rotate (or barely rotates) under load. Plastic indentation is then decisive. Static/dynamic refers to rotation, not to how the load changes over time.")
add(B, "tf", "Die [oanord] hat eine größere [stuetzbasis] und ist kippsteifer als die [xanord].",
    "The [oanord] has a larger [stuetzbasis] and is stiffer against tilting than the [xanord].", None, True,
    "Richtig. In der O-Anordnung zeigen die Drucklinien nach außen, die Stützbasis wird größer. Die X-Anordnung ist weniger steif, lässt aber mehr Winkelfehler zu.",
    "Correct. In the O-arrangement the pressure lines point outwards, which enlarges the support distance. The X-arrangement is less stiff but tolerates more angular error.")
add(B, "match", "Ordne die Kurzzeichen ihrer Bedeutung zu.", "Match the designation codes to their meaning.",
    {"left": [O("K"), O("S"), O("C3"), O("P5"), O("Z")],
     "right": [O("Käfig mit Wälzkörpern", "Cage with rolling elements"),
               O("Nichtrostender Stahl", "Stainless steel"),
               O("[lagerspiel] größer als normal", "[lagerspiel^] larger than normal"),
               O("Toleranz enger als normal", "Tolerance tighter than normal"),
               O("Eine [deckscheibe]", "One [deckscheibe]")]},
    None,
    "Vorsetzzeichen (K, L, R, S) kennzeichnen Einzelteile oder den Werkstoff. Nachsetzzeichen (C2, C3, P5, MA, RS, Z …) kennzeichnen Abweichungen von der Standardausführung (DIN 623).",
    "Prefixes (K, L, R, S) identify individual parts or the material. Suffixes (C2, C3, P5, MA, RS, Z …) identify deviations from the standard design (DIN 623).")
add(B, "mc", "Welche Lagerung ist am einfachsten und günstigsten, legt die Welle axial aber nicht genau fest (sie „schwimmt“)?",
    "Which arrangement is the simplest and cheapest, but does not define the shaft position exactly (the shaft 'floats')?",
    [O("[fll]"), O("[schwl]"), O("[angl] in O", "[angl] in O"), O("[angl] in X", "[angl] in X")], 1,
    "Bei der [schwl] hat die Welle ein definiertes Axialspiel von ca. 0,5 … 1 mm. Sie ist einfach und günstig, aber nicht für wechselnde Axialkräfte geeignet.",
    "In a [schwl] the shaft has a defined axial play of approx. 0.5 … 1 mm. It is simple and cheap, but not suitable for alternating axial loads.")
add(B, "mc", "Welche Berührung haben Rollenlager zwischen [waelzk] und Laufbahn?",
    "What kind of contact do roller bearings have between [waelzk] and raceway?",
    [O("[punktber]", "[punktber^]"), O("[linienber]", "[linienber^]"), O("Flächenberührung", "Surface contact"), O("Keine, nur Schmierfilm", "None, only a lubricant film")], 1,
    "Rollen haben [linienber] und tragen deshalb radial mehr als vergleichbare Kugellager. Kugeln haben [punktber].",
    "Rollers have [linienber] and therefore carry more radial load than comparable ball bearings. Balls have [punktber].")

# ---------------- Getriebe / Zahnräder ----------------
Z = "gears"
FL = ("Welche Verzahnung (Verlauf der [flankenlinie]) ist dargestellt? (Seitenansicht zweier Stirnräder)",
      "Which gearing (course of the [flankenlinie]) is shown? (side view of two spur gears)")
FLO = [O("[gerade]"), O("[schraeg]"), O("[pfeil]"), O("[doppel]")]
add(Z, "img", FL[0], FL[1], FLO, 0,
    "[gerade]: Die Flankenlinien verlaufen parallel zur Radachse. Sie ist robust und einfach herzustellen, läuft aber lauter, weil die Zähne stoßartig eingreifen.",
    "[gerade^]: the flank lines run parallel to the gear axis. It is robust and easy to make, but noisier because the teeth engage abruptly.",
    image="img/zahnrad_gerade.svg")
add(Z, "img", FL[0], FL[1], FLO, 1,
    "[schraeg]: Die Flankenlinien liegen schräg (Schrägungswinkel β). Die Zähne greifen allmählich ein, das Getriebe läuft ruhiger und trägt mehr, erzeugt aber eine [axialkraft].",
    "[schraeg^]: the flank lines are inclined (helix angle β). The teeth engage gradually, so the gearbox runs more smoothly and carries more load, but it creates an [axialkraft].",
    image="img/zahnrad_schraeg.svg")
add(Z, "img", FL[0], FL[1], FLO, 2,
    "[pfeil]: zwei gegensinnig schräge Zahnreihen ohne Zwischennut. Die Axialkräfte heben sich gegenseitig auf.",
    "[pfeil^]: two oppositely inclined rows of teeth without a groove between them. The axial forces cancel each other out.",
    image="img/zahnrad_pfeil.svg")
add(Z, "img", FL[0], FL[1], FLO, 3,
    "[doppel]: zwei gegensinnig schräge Zahnreihen mit einer Nut dazwischen (Werkzeugauslauf). Auch hier heben sich die Axialkräfte auf.",
    "[doppel^]: two oppositely inclined rows of teeth with a groove between them (tool runout). Here too the axial forces cancel out.",
    image="img/zahnrad_doppelschraeg.svg")
GT = ("Welche Getriebeart ist dargestellt?", "Which type of gear drive is shown?")
GTO = [O("[stirnrad]"), O("[kegelrad]"), O("[schnecke]"), O("Getriebe mit [zahnstange]", "[zahnstange^] and pinion drive")]
add(Z, "img", GT[0], GT[1], GTO, 1,
    "[kegelrad]: Die Achsen schneiden sich (meist unter 90°), die Räder sind kegelförmig. Die gestrichelte Linie zeigt die gemeinsame Kegelmantellinie zur Kegelspitze.",
    "[kegelrad^]: the axes intersect (usually at 90°) and the gears are conical. The dashed line marks the common cone generator leading to the cone apex.",
    image="img/zahnrad_kegelrad.svg")
add(Z, "img", GT[0], GT[1], GTO, 2,
    "[schnecke]: Die Achsen von Schnecke und Schneckenrad kreuzen sich, ohne sich zu schneiden. Damit sind große Übersetzungen in einer Stufe möglich.",
    "[schnecke^]: the axes of worm and worm wheel cross without intersecting. This allows large transmission ratios in a single stage.",
    image="img/zahnrad_schnecke.svg")
add(Z, "img", GT[0], GT[1], GTO, 3,
    "Getriebe mit [zahnstange] und Ritzel: Es wandelt eine Drehbewegung in eine geradlinige Bewegung um oder umgekehrt.",
    "[zahnstange^] and pinion drive: it converts rotation into linear motion or vice versa.",
    image="img/zahnrad_zahnstange.svg")
add(Z, "img", "Wie heißt das große, innenverzahnte Rad in dieser Abbildung?",
    "What is the large internally toothed gear in this figure called?",
    [O("[ritzel]", "[ritzel^]"), O("[hohlrad]", "[hohlrad^]"), O("Schneckenrad", "Worm wheel"), O("[zahnstange]", "[zahnstange^]")], 1,
    "Ein innenverzahntes Rad heißt [hohlrad]. Mit einem außenverzahnten [ritzel] bildet es ein Innen-Stirnradgetriebe mit parallelen Achsen und gleicher Drehrichtung.",
    "An internally toothed gear is called an [hohlrad]. Together with an external [ritzel] it forms an internal spur gear drive with parallel axes and the same direction of rotation.",
    image="img/zahnrad_hohlrad.svg")
add(Z, "mc", "Welcher Nachteil hat die [schraeg] gegenüber der [gerade]?",
    "What is a disadvantage of [schraeg] compared to [gerade]?",
    [O("Lauterer Lauf", "Noisier operation"), O("Geringere Tragfähigkeit", "Lower load capacity"),
     O("Zusätzliche [axialkraft]", "Additional [axialkraft]"), O("Kleinere [ueberdeckung]", "Smaller [ueberdeckung]")], 2,
    "Schrägverzahnung läuft ruhiger, trägt mehr und hat eine größere Überdeckung. Sie erzeugt aber eine [axialkraft], die die Lager aufnehmen müssen.",
    "Helical gearing runs more smoothly, carries more load and has a larger contact ratio. However, it creates an [axialkraft] that the bearings must absorb.")
add(Z, "mc", "Warum verwendet man [pfeil] oder [doppel]?",
    "Why is [pfeil] or [doppel] used?",
    [O("Weil sie einfacher herzustellen ist", "Because it is easier to manufacture"),
     O("Weil sich die Axialkräfte der beiden Zahnhälften aufheben", "Because the axial forces of both tooth halves cancel out"),
     O("Weil sie eine größere Übersetzung erlaubt", "Because it allows a larger transmission ratio"),
     O("Weil kein Schmierstoff nötig ist", "Because no lubricant is needed")], 1,
    "Die beiden gegensinnig schrägen Hälften erzeugen entgegengesetzte Axialkräfte. Man nutzt also die Laufruhe der Schrägverzahnung ohne Axiallast auf die Lager.",
    "The two oppositely inclined halves produce opposite axial forces. You get the smooth running of helical gearing without axial load on the bearings.")
add(Z, "match", "Ordne jedem Getriebe die Lage seiner Achsen bzw. seine Funktion zu.",
    "Match each gear drive to its axis arrangement or function.",
    {"left": [O("[stirnrad]"), O("[kegelrad]"), O("[schnecke]"), O("[zahnstange] und [ritzel]", "[zahnstange^] and [ritzel]")],
     "right": [O("Parallele Achsen", "Parallel axes"),
               O("Sich schneidende Achsen", "Intersecting axes"),
               O("Gekreuzte Achsen, große Übersetzung", "Crossed axes, large transmission ratio"),
               O("Drehbewegung ↔ Längsbewegung", "Rotation ↔ linear motion")]},
    None,
    "Stirnrad: parallele Achsen. Kegelrad: sich schneidende Achsen. Schnecke (und Hypoid): gekreuzte Achsen. Zahnstange: wandelt Dreh- in Längsbewegung.",
    "Spur gear: parallel axes. Bevel gear: intersecting axes. Worm (and hypoid): crossed axes. Rack: converts rotation into linear motion.")
add(Z, "mc", "Welcher [eingriffsw] α ist nach DIN 867 genormt?", "Which [eingriffsw] α is standardized according to DIN 867?",
    [O("14,5°", "14.5°"), O("15°"), O("20°"), O("30°")], 2,
    "Das Bezugsprofil nach DIN 867 hat einen [eingriffsw] von α = 20°.",
    "The reference profile according to DIN 867 has a [eingriffsw] of α = 20°.")
add(Z, "mc", "Wie hängen [teilkreis]-Durchmesser d, [modul] m und [zahnzahl] z zusammen?",
    "How are [teilkreis] diameter d, [modul] m and [zahnzahl] z related?",
    [O("d = m · z"), O("d = m / z"), O("d = z / m"), O("d = π · z / m")], 0,
    "d = m · z. Der Modul ist das Maß für die Zahngröße (m = p/π). Bei gleicher Zähnezahl hat ein größerer Modul also einen größeren Durchmesser.",
    "d = m · z. The module is the measure of tooth size (m = p/π), so with the same number of teeth a larger module gives a larger diameter.")
add(Z, "mc", "Wie berechnet man die [uebers] i einer Zahnradstufe (1 = treibendes Rad, 2 = getriebenes Rad)?",
    "How is the [uebers] i of a gear stage calculated (1 = driving gear, 2 = driven gear)?",
    [O("i = z₁ / z₂ = n₂ / n₁"), O("i = z₂ / z₁ = n₁ / n₂"), O("i = z₁ · z₂"), O("i = n₁ · n₂")], 1,
    "i = n₁ / n₂ = z₂ / z₁. Treibt ein kleines Ritzel ein großes Rad, ist i > 1: Die Drehzahl sinkt, das Moment steigt.",
    "i = n₁ / n₂ = z₂ / z₁. If a small pinion drives a large gear, i > 1: speed decreases and torque increases.")
add(Z, "mc", "Warum hat sich die [evolvente] im Maschinenbau durchgesetzt?",
    "Why has [evolvente] become established in mechanical engineering?",
    [O("Sie rollt ganz ohne Gleiten ab", "It rolls without any sliding"),
     O("Sie ist unempfindlich gegen Änderungen des [achsabstand]s und günstig herzustellen", "It is insensitive to changes in [achsabstand] and cheap to manufacture"),
     O("Sie braucht keine Schmierung", "It needs no lubrication"),
     O("Sie hat eine veränderliche Übersetzung", "It has a variable transmission ratio")], 1,
    "Die Evolvente ist günstig herzustellen (gerade Werkzeugflanken), hält die Übersetzung konstant und reagiert kaum auf Achsabstandsänderungen. Ein gewisses Gleiten (Verschleiß) bleibt.",
    "The involute is cheap to manufacture (straight tool flanks), keeps the transmission ratio constant and is insensitive to center distance changes. Some sliding (wear) remains.")
add(Z, "tf", "Die abgebildete [zykloide] (Flanken entstehen durch Abrollen von Rollkreisen auf dem Grundkreis) ist unempfindlich gegen Änderungen des [achsabstand]s.",
    "The [zykloide] shown (flanks generated by rolling circles on the base circle) is insensitive to changes in [achsabstand].", None, False,
    "Falsch. Die Flanken entstehen durch Abrollen eines Rollkreises außen (Epizykloide) und innen (Hypozykloide) auf dem Grundkreis. Die Verzahnung rollt fast ohne Gleiten ab, reagiert aber empfindlich auf Achsabstandsänderungen. Man findet sie z. B. in Feinwerktechnik und Uhren.",
    "False. The flanks are generated by a rolling circle rolling outside (epicycloid) and inside (hypocycloid) the base circle. The gearing rolls with almost no sliding but is sensitive to center distance changes. It is used e.g. in precision devices and clocks.",
    image="img/foto_zykloide.jpg", source="YouTube, www.youtube.com/watch?v=c0LSoBxfOq0 · Skript FME, Folie 27")
add(Z, "mc", "Welchen Mindestwert muss die [ueberdeckung] εα haben?", "What minimum value must the [ueberdeckung] εα have?",
    [O("0,5", "0.5"), O("1"), O("2"), O("π")], 1,
    "εα ≥ 1, damit in jeder Stellung mindestens ein Zahnpaar im Eingriff ist. Bei εα < 1 entsteht Spiel und das Getriebe klappert bei Drehrichtungswechsel.",
    "εα ≥ 1, so that at least one tooth pair is in mesh at every position. With εα < 1 backlash occurs and the gearbox rattles when the direction of rotation changes.")
add(Z, "mc", "Welcher Punkt ist KEIN Grund für eine [profilv]?", "Which of these is NOT a reason for [profilv]?",
    [O("Anpassung an einen vorgegebenen [achsabstand]", "Adapting to a given [achsabstand]"),
     O("Erhöhung der Tragfähigkeit am [zahnfuss]", "Increasing the load capacity at the [zahnfuss]"),
     O("Vermeidung von [unterschnitt]", "Avoiding [unterschnitt]"),
     O("Änderung der [uebers]", "Changing the [uebers]")], 3,
    "Die Profilverschiebung nutzt nur einen anderen Bereich derselben Evolvente. Die Übersetzung bleibt deshalb unverändert.",
    "Profile shift only uses a different part of the same involute. The transmission ratio therefore stays the same.")
add(Z, "tf", "Eine positive [profilv] (V-Plus) verstärkt den [zahnfuss] und schwächt den [zahnkopf].",
    "A positive [profilv] (V-plus) strengthens the [zahnfuss] and weakens the [zahnkopf].", None, True,
    "Richtig. Der Zahnfuß wird dicker, der Kopf dünner. Grenze ist ein zu spitzer Zahnkopf; bei negativer Verschiebung droht Unterschnitt.",
    "Correct. The root gets thicker and the tip thinner. The limit is an overly pointed tip; negative shift risks undercut.")
add(Z, "mc", "An den Zahnflanken entstehen durch Ermüdung kleine Materialausbrüche. Wie heißt dieses Schadensbild?",
    "Small material break-outs appear on the tooth flanks due to fatigue. What is this failure called?",
    [O("[fressen]", "[fressen^]"), O("[zfbruch]", "[zfbruch^]"), O("[gruebchen]", "[gruebchen^]"), O("[grauf]", "[grauf^]")], 2,
    "Grübchen (Pitting) entstehen durch hohe wechselnde Pressungen an der Flanke (Flankentragfähigkeit, DIN 3990 / ISO 6336).",
    "Pitting is caused by high alternating contact pressures on the flank (flank load capacity, DIN 3990 / ISO 6336).")
add(Z, "mc", "Die Zahnflanken verschweißen kurzzeitig und reißen wieder auf, weil der Schmierfilm thermisch versagt. Welches Schadensbild ist das?",
    "The tooth flanks briefly weld together and tear apart because the lubricant film fails thermally. Which failure is this?",
    [O("[fressen]", "[fressen^]"), O("[gruebchen]", "[gruebchen^]"), O("[grauf]", "[grauf^]"), O("Verschleiß durch Unterschnitt", "Wear due to undercut")], 0,
    "Beim Fressen versagen Schmierstoff und Schutzschichten durch zu hohe Temperatur im Kontakt. Die Flanken werden großflächig zerstört. Gleiche Härte beider Räder bei ungehärteten Flanken fördert Fressen.",
    "During scuffing the lubricant and protective layers fail due to excessive contact temperature. The flanks are destroyed over large areas. Equal hardness of both gears with unhardened flanks promotes scuffing.")
add(Z, "match", "Ordne die Zahnradschäden ihrer Beschreibung zu.", "Match the gear failures to their description.",
    {"left": [O("[gruebchen]", "[gruebchen^]"), O("[zfbruch]", "[zfbruch^]"), O("[fressen]", "[fressen^]"), O("[grauf]", "[grauf^]")],
     "right": [O("Ermüdungsausbrüche auf der Flanke", "Fatigue break-outs on the flank"),
               O("Riss im Zahnfuß, Zahn bricht ab", "Crack at the tooth root, tooth breaks off"),
               O("Verschweißen und Aufreißen der Flanken", "Flanks weld together and tear apart"),
               O("Mikroermüdung, grau schimmernde Flächen", "Micro-fatigue, grey shaded areas")]},
    None,
    "Die vier Hauptschadensarten aus der Vorlesung: Grübchen (Flanke), Zahnfußbruch (Fuß), Fressen (Schmierfilmversagen), Graufleckigkeit (Mikroermüdung).",
    "The four main failure types from the lecture: pitting (flank), tooth root breakage (root), scuffing (lubricant film failure), micropitting (micro-fatigue).")
add(Z, "mc", "Wie ergibt sich die Gesamtübersetzung eines mehrstufigen Getriebes?",
    "How is the total transmission ratio of a multi-stage gearbox obtained?",
    [O("i_ges = i₁ + i₂ + …", "i_total = i₁ + i₂ + …"), O("i_ges = i₁ · i₂ · …", "i_total = i₁ · i₂ · …"),
     O("i_ges = größte Einzelübersetzung", "i_total = largest single ratio"), O("i_ges = (i₁ + i₂) / 2", "i_total = (i₁ + i₂) / 2")], 1,
    "Die Einzelübersetzungen werden multipliziert. Dasselbe gilt für die Wirkungsgrade: η_ges = η₁ · η₂ · …",
    "The individual ratios are multiplied. The same applies to efficiencies: η_total = η₁ · η₂ · …")
add(Z, "mc", "Wie berechnet man das Abtriebsmoment T₂ aus dem Antriebsmoment T₁, der [uebers] i und dem [wirkungsgrad] η?",
    "How is the output torque T₂ calculated from the input torque T₁, the [uebers] i and the [wirkungsgrad] η?",
    [O("T₂ = η · i · T₁"), O("T₂ = T₁ / (η · i)"), O("T₂ = η · T₁ / i"), O("T₂ = i · T₁ / η")], 0,
    "T₂ = η · i · T₁. Aus P = T · ω folgt: Wird die Drehzahl um i reduziert, steigt das Moment um i; der Wirkungsgrad η < 1 mindert es etwas.",
    "T₂ = η · i · T₁. From P = T · ω: if speed is reduced by i, torque rises by i; the efficiency η < 1 reduces it somewhat.")
add(Z, "mc", "Wie berechnet man die [tangkraft] Ft am Zahnrad aus Drehmoment T und [teilkreis]-Durchmesser d?",
    "How is the [tangkraft] Ft on a gear calculated from torque T and [teilkreis] diameter d?",
    [O("Ft = T · d"), O("Ft = 2 · T / d"), O("Ft = T / (2 · d)"), O("Ft = d / T")], 1,
    "Ft = T / r = 2 · T / d. Die Radialkraft folgt daraus mit Fr = Ft · tan α.",
    "Ft = T / r = 2 · T / d. The radial force follows as Fr = Ft · tan α.")
add(Z, "tf", "Das [ritzel] sollte den festeren Werkstoff bekommen, weil es mehr Lastwechsel erfährt als das große Rad.",
    "The [ritzel] should get the stronger material because it experiences more load cycles than the large gear.", None, True,
    "Richtig. Das kleine Rad dreht schneller und jeder Zahn wird öfter belastet. Werkstoff und Wärmebehandlung trotzdem nur so hochwertig wie nötig wählen.",
    "Correct. The small gear turns faster and each tooth is loaded more often. Still, choose material and heat treatment only as high-grade as necessary.")
add(Z, "tf", "Zahnradgetriebe bieten von sich aus einen Überlastschutz.",
    "Gear drives provide overload protection by themselves.", None, False,
    "Falsch. Zahnradgetriebe übertragen formschlüssig und schlupffrei. Deshalb haben sie keinen Überlastschutz; dafür braucht man z. B. eine Rutschkupplung.",
    "False. Gear drives transmit by form fit and without slip. That is why they have no overload protection; you need e.g. a slip clutch for that.")
add(Z, "mc", "Ab welcher [zahnzahl] tritt bei geradverzahnten Stirnrädern (ohne Profilverschiebung) theoretisch kein [unterschnitt] mehr auf?",
    "From which [zahnzahl] does [unterschnitt] theoretically no longer occur on straight-cut spur gears (without profile shift)?",
    [O("z ≥ 7"), O("z ≥ 14"), O("z ≥ 17"), O("z ≥ 25")], 2,
    "Die theoretische Grenzzähnezahl ist 17, praktisch genügen etwa 14. Bei weniger Zähnen hilft eine positive Profilverschiebung.",
    "The theoretical limit is 17 teeth; in practice about 14 is enough. With fewer teeth, a positive profile shift helps.")

if __name__ == "__main__":
    import json, sys
    json.dump(Q, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(Q), "Fragen;", sum(q["topic_id"] == B for q in Q), "Lager,", sum(q["topic_id"] == Z for q in Q), "Getriebe")
