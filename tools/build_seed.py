"""Erzeugt supabase/02_fragen_<name>.sql aus einer Fragen-JSON-Datei.
Fragen werden nur eingefügt, wenn das jeweilige Thema noch leer ist
(so überschreibt ein erneutes Ausführen keine Änderungen aus dem Admin-Bereich)."""
import json, sys
from collections import OrderedDict

src, dst = sys.argv[1], sys.argv[2]
BY_IMAGE = "--by-image" in sys.argv  # je Frage einfügen, wenn ihr Bild noch nicht verwendet wird
qs = json.load(open(src, encoding="utf-8"))

def lit(v):
    if v is None:
        return "null"
    s = v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)
    tag = "$q$"
    assert tag not in s
    return f"{tag}{s}{tag}"

by_topic = OrderedDict()
for q in qs:
    by_topic.setdefault(q["topic_id"], []).append(q)

out = ["-- Automatisch erzeugt mit tools/build_seed.py – Fragen für: " + ", ".join(by_topic), ""]
for topic, items in by_topic.items():
    out.append("do $seed$ begin")
    if not BY_IMAGE:
        out.append(f"if not exists (select 1 from public.questions where topic_id = '{topic}') then")
    for q in items:
        if BY_IMAGE:
            out.append(f"if not exists (select 1 from public.questions where image = {lit(q['image'])}) then")
        out.append(
            "insert into public.questions (topic_id, qtype, prompt_de, prompt_en, image, image_source, options, correct, explanation_de, explanation_en) values ("
            + ", ".join([lit(q["topic_id"]), lit(q["qtype"]), lit(q["prompt_de"]), lit(q["prompt_en"]), lit(q.get("image")), lit(q.get("image_source")),
                         (lit(q["options"]) + "::jsonb") if q.get("options") is not None else "null",
                         (lit(q["correct"]) + "::jsonb") if q.get("correct") is not None else "null",
                         lit(q["explanation_de"]), lit(q["explanation_en"])])
            + ");")
        if BY_IMAGE:
            out.append("end if;")
    if not BY_IMAGE:
        out.append("end if;")
    out.append("end $seed$;")
    out.append("")
open(dst, "w", encoding="utf-8").write("\n".join(out))
print("geschrieben:", dst, len(qs), "Fragen")
