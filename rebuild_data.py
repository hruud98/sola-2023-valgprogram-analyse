#!/usr/bin/env python3
"""Rebuild detaljert_gradering.csv + gradering_sammendrag.(csv|json) from
per-policy data: existing detailed rows (AP/KrF/SV) + _raw/*.txt (5 parties)."""
import csv
import json
import os
import re

HER = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HER, "_raw")
DETALJ = os.path.join(HER, "detaljert_gradering.csv")

META = {  # forkortelse, full navn
    "Arbeiderpartiet": ("AP", "Arbeiderpartiet"),
    "Kristelig Folkeparti": ("KrF", "Kristelig Folkeparti"),
    "Sosialistisk Venstreparti": ("SV", "Sosialistisk Venstreparti"),
    "Hoyre": ("H", "Høyre"),
    "FrP": ("FrP", "Fremskrittspartiet"),
    "INP": ("INP", "Industri- og Næringspartiet"),
    "MDG": ("MDG", "Miljøpartiet De Grønne"),
    "Venstre": ("V", "Venstre"),
}

# parti(full) -> list of (score, text)
data = {}

# 1) existing detailed rows for AP/KrF/SV
with open(DETALJ, encoding="utf-8") as f:
    for row in csv.DictReader(f, delimiter=";"):
        data.setdefault(row["parti"], []).append((int(row["score"]), row["lofte"]))

# 2) the five raw files
for key in ("Hoyre", "FrP", "INP", "MDG", "Venstre"):
    navn = META[key][1]
    data[navn] = []
    with open(os.path.join(RAW, f"{key}.txt"), encoding="utf-8") as f:
        for line in f:
            m = re.match(r"^\s*([1-5])\|(.*)$", line.rstrip("\n"))
            if m:
                tekst = m.group(2).replace(";", ",").strip()
                data[navn].append((int(m.group(1)), tekst))

# rebuild forkortelse lookup by full name
fork = {full: ab for ab, full in META.values()}

# write detaljert_gradering.csv (all 8)
rekkefolge = ["Arbeiderpartiet", "Høyre", "Fremskrittspartiet",
              "Sosialistisk Venstreparti", "Kristelig Folkeparti", "Venstre",
              "Miljøpartiet De Grønne", "Industri- og Næringspartiet"]
with open(DETALJ, "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["parti", "score", "lofte"])
    for navn in rekkefolge:
        for score, tekst in data[navn]:
            w.writerow([navn, score, tekst])

# summary
sammendrag = []
for navn in rekkefolge:
    rows = data[navn]
    n = len(rows)
    dist = [sum(1 for s, _ in rows if s == i) for i in range(1, 6)]
    snitt = sum(s for s, _ in rows) / n
    hoy = (dist[3] + dist[4]) / n * 100
    lav = (dist[0] + dist[1]) / n * 100
    sammendrag.append({
        "parti": navn, "forkortelse": fork[navn], "antall": n,
        "fordeling": dist, "snitt": round(snitt, 2),
        "andel_hoy_4_5": round(hoy, 1), "andel_lav_1_2": round(lav, 1),
    })

with open(os.path.join(HER, "gradering_sammendrag.csv"), "w",
          encoding="utf-8", newline="") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["parti", "forkortelse", "antall", "score1", "score2", "score3",
                "score4", "score5", "snitt", "andel_hoy_4_5", "andel_lav_1_2"])
    for r in sammendrag:
        w.writerow([r["parti"], r["forkortelse"], r["antall"], *r["fordeling"],
                    r["snitt"], r["andel_hoy_4_5"], r["andel_lav_1_2"]])

with open(os.path.join(HER, "gradering_sammendrag.json"), "w",
          encoding="utf-8") as f:
    json.dump(sammendrag, f, indent=2, ensure_ascii=False)

total = sum(r["antall"] for r in sammendrag)
print(f"Totalt antall løfter: {total}")
for r in sorted(sammendrag, key=lambda x: x["snitt"], reverse=True):
    print(f"  {r['forkortelse']:>4}  n={r['antall']:>3}  snitt={r['snitt']}  "
          f"høy={r['andel_hoy_4_5']}%")
