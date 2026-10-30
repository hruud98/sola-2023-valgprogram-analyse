# Gradering: Hvor konkrete er partienes valgløfter? (Sola 2023)

Analyse av hvor **konkrete/målbare** vs **generelle/vage** valgløftene er i
programmene til åtte partier ved kommunevalget i Sola 2023.

## Skala (1–5)
| Score | Betydning |
|------:|-----------|
| 1 | Svært generell / vag (ren verdi- eller holdningserklæring) |
| 2 | Overveiende generell |
| 3 | Middels – retning angitt, men lite målbart |
| 4 | Overveiende konkret |
| 5 | Svært konkret / målbar (tall, frist, konkret tiltak) |

Snitt er regnet ut fra fordelingen (sum av score / antall løfter).

## Hovedfunn
- **726 løfter** gradert totalt på tvers av åtte partier.
- **SV er mest konkret** (snitt **3,29**; 46 % av løftene på nivå 4–5).
- **INP er minst konkret** (snitt **2,58**; 55 % av løftene på nivå 1–2).
- De fleste partiene ligger tett i intervallet **2,6–3,0** – altså overveiende
  retningsgivende, men i begrenset grad målbare løfter.

## Filer
| Fil | Innhold |
|-----|---------|
| `gradering_sammendrag.csv` | Oppsummering per parti (antall, fordeling 1–5, snitt, andel høy/lav) |
| `gradering_sammendrag.json` | Samme data som JSON |
| `detaljert_gradering.csv` | Løfte-for-løfte score for AP, KrF og SV (full linjedata tilgjengelig) |
| `graf_snitt_konkret.png` | Snitt konkretiseringsgrad per parti (NRK-stil, partifarger) |
| `graf_fordeling_1_5.png` | Stablet fordeling av score 1–5 per parti |
| `lag_grafer.py` | Script som genererer begge grafene |

## Forbehold
- **Detaljert linjedata** (`detaljert_gradering.csv`) finnes kun for **AP, KrF og SV**.
  For de fem øvrige partiene (Høyre, FrP, INP, MDG, Venstre) er kun aggregert
  fordeling tilgjengelig.
- Gradering er skjønnsmessig og gjort per løftesetning; antall løfter avhenger
  av hvor fint programteksten er splittet.
- Partimarkører i grafen bruker ensartede fargede partisirkler med forkortelse
  (offisielle partifarger), ikke nedlastede logoer, for et rent og konsekvent uttrykk.

## Kjøre på nytt
```bash
python3 -m venv .venv
./.venv/bin/python -m pip install matplotlib
./.venv/bin/python lag_grafer.py
```
