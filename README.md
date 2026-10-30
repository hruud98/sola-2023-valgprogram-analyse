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
- **745 løfter** gradert totalt på tvers av åtte partier.
- **INP er mest konkret** (snitt **3,54**; 50 % av løftene på nivå 4–5),
  tett fulgt av **MDG** (snitt **3,51**) og **SV** (snitt **3,29**).
- **Høyre er minst konkret** (snitt **2,76**), med Venstre og KrF like bak.
- Spennet er større enn først antatt: fra 2,76 (H) til 3,54 (INP).

## Filer
| Fil | Innhold |
|-----|---------|
| `gradering_sammendrag.csv` | Oppsummering per parti (antall, fordeling 1–5, snitt, andel høy/lav) |
| `gradering_sammendrag.json` | Samme data som JSON |
| `detaljert_gradering.csv` | Løfte-for-løfte score for alle åtte partiene (745 rader) |
| `graf_snitt_konkret.png` | Snitt konkretiseringsgrad per parti (NRK-stil, partifarger) |
| `graf_andel_hoy_4_5.png` | Andel løfter på nivå 4–5 per parti |
| `graf_fordeling_1_5.png` | Stablet fordeling av score 1–5 per parti |
| `lag_grafer.py` | Script som genererer grafene |
| `rebuild_data.py` | Bygger sammendrag + detaljert CSV fra per-løfte-data |

## Forbehold
- **Detaljert linjedata** (`detaljert_gradering.csv`) finnes nå for **alle åtte partiene**.
- Gradering er skjønnsmessig og gjort per løftesetning; antall løfter avhenger
  av hvor fint programteksten er splittet.
- De fem partiene Høyre, FrP, INP, MDG og Venstre ble gradert i en egen, senere
  kjøring enn AP/KrF/SV. En uavhengig re-gradering kan gi noe ulikt resultat,
  særlig der et program har mange korte, konkrete punktlister.
- Partimarkører i grafen bruker ensartede fargede partisirkler med forkortelse
  (offisielle partifarger), ikke nedlastede logoer, for et rent og konsekvent uttrykk.

## Kjøre på nytt
```bash
python3 -m venv .venv
./.venv/bin/python -m pip install matplotlib
./.venv/bin/python lag_grafer.py
```
