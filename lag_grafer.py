#!/usr/bin/env python3
"""
Sola 2023 – visualisering av hvor konkrete/målbare partienes valgløfter er.
Gradering 1–5:  1 = svært generell/vag,  5 = svært konkret/målbar.

Lager to NRK-inspirerte grafer:
  1) graf_snitt_konkret.png      – gjennomsnittlig konkretiseringsgrad per parti
  2) graf_fordeling_1_5.png      – stablet fordeling av score 1–5 per parti

Logoer (valgfritt) leses fra mappen  logos/<FORKORTELSE>.png .
Mangler en logo, tegnes en farget sirkel med partiforkortelsen i stedet.
"""
from __future__ import annotations
import csv
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.image as mpimg

HER = os.path.dirname(os.path.abspath(__file__))
CSV = os.path.join(HER, "gradering_sammendrag.csv")
LOGO_DIR = os.path.join(HER, "logos")

# Offisielle/innarbeidede partifarger
FARGE = {
    "AP": "#E3000F",
    "H": "#007AC8",
    "FrP": "#005F9E",
    "SV": "#C6093B",
    "KrF": "#F9B000",
    "V": "#137B80",
    "MDG": "#4B9B3B",
    "INP": "#F07D00",
}

# Gråtoner for score 1–5 i fordelingsgrafen (lys = vag, mørk = konkret) med aksent
SCORE_FARGE = ["#D9D9D9", "#AEB8BF", "#7FA8C9", "#3F7CAC", "#13304A"]


def les_data():
    rader = []
    with open(CSV, encoding="utf-8") as f:
        for r in csv.DictReader(f, delimiter=";"):
            r["antall"] = int(r["antall"])
            r["snitt"] = float(r["snitt"])
            r["andel_hoy_4_5"] = float(r["andel_hoy_4_5"])
            r["dist"] = [int(r[f"score{i}"]) for i in range(1, 6)]
            rader.append(r)
    return rader


def legg_logo(ax, forkortelse, x, y, zoom=0.5):
    # Ensartet NRK-stil: farget partisirkel med forkortelse (tydelig og lesbart).
    ax.scatter([x], [y], s=1500, color=FARGE.get(forkortelse, "#444"),
               zorder=5, clip_on=False)
    ax.annotate(forkortelse, (x, y), ha="center", va="center",
                color="white", fontsize=10, fontweight="bold", zorder=6,
                clip_on=False, annotation_clip=False)
    return False


def graf_snitt(rader):
    rader = sorted(rader, key=lambda r: r["snitt"], reverse=True)
    fig, ax = plt.subplots(figsize=(11, 6.5))
    xs = range(len(rader))
    verdier = [r["snitt"] for r in rader]
    farger = [FARGE.get(r["forkortelse"], "#888") for r in rader]
    bars = ax.bar(xs, verdier, color=farger, width=0.68, zorder=3)

    for i, (r, v) in enumerate(zip(rader, verdier)):
        ax.annotate(f"{v:.2f}", (i, v), ha="center", va="bottom",
                    fontsize=13, fontweight="bold", xytext=(0, 6),
                    textcoords="offset points", color="#222")
        legg_logo(ax, r["forkortelse"], i, -0.22, zoom=0.5)

    ax.axhline(3.0, color="#999", lw=1, ls="--", zorder=2)
    ax.annotate("Midtpunkt (3,0)", (len(rader) - 0.5, 3.0), ha="right",
                va="bottom", color="#777", fontsize=9)

    ax.set_ylim(0, 5)
    ax.set_yticks(range(0, 6))
    ax.set_xlim(-0.6, len(rader) - 0.4)
    ax.set_xticks([])
    ax.set_ylabel("Gjennomsnittlig konkretiseringsgrad (1–5)", fontsize=11)
    ax.set_title("Hvor konkrete er partienes valgløfter i Sola 2023?",
                 fontsize=16, fontweight="bold", loc="left", pad=16)
    ax.text(0, 1.02,
            "1 = svært generell / vag løftetekst      5 = svært konkret / målbar løftetekst",
            transform=ax.transAxes, fontsize=10, color="#666")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.spines["left"].set_color("#ccc")
    ax.spines["bottom"].set_color("#ccc")
    ax.tick_params(length=0)
    ax.grid(axis="y", color="#eee", zorder=0)
    fig.subplots_adjust(bottom=0.12, top=0.84)
    ut = os.path.join(HER, "graf_snitt_konkret.png")
    fig.savefig(ut, dpi=160, bbox_inches="tight")
    print("Lagret", ut)


def graf_andel_hoy(rader):
    rader = sorted(rader, key=lambda r: r["andel_hoy_4_5"], reverse=True)
    fig, ax = plt.subplots(figsize=(11, 6.5))
    xs = range(len(rader))
    verdier = [r["andel_hoy_4_5"] for r in rader]
    farger = [FARGE.get(r["forkortelse"], "#888") for r in rader]
    ax.bar(xs, verdier, color=farger, width=0.68, zorder=3)

    for i, (r, v) in enumerate(zip(rader, verdier)):
        ax.annotate(f"{v:.1f}%", (i, v), ha="center", va="bottom",
                    fontsize=13, fontweight="bold", xytext=(0, 6),
                    textcoords="offset points", color="#222")
        legg_logo(ax, r["forkortelse"], i, -2.6, zoom=0.5)

    ymax = max(verdier) * 1.18
    ax.set_ylim(0, ymax)
    ax.set_xlim(-0.6, len(rader) - 0.4)
    ax.set_xticks([])
    ax.set_ylabel("Andel løfter på nivå 4–5 (%)", fontsize=11)
    ax.set_title("Andel konkrete/målbare valgløfter (nivå 4–5) i Sola 2023",
                 fontsize=16, fontweight="bold", loc="left", pad=16)
    ax.text(0, 1.02,
            "Nivå 4–5 = overveiende til svært konkrete / målbare løfter",
            transform=ax.transAxes, fontsize=10, color="#666")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.spines["left"].set_color("#ccc")
    ax.spines["bottom"].set_color("#ccc")
    ax.tick_params(length=0)
    ax.grid(axis="y", color="#eee", zorder=0)
    fig.subplots_adjust(bottom=0.12, top=0.84)
    ut = os.path.join(HER, "graf_andel_hoy_4_5.png")
    fig.savefig(ut, dpi=160, bbox_inches="tight")
    print("Lagret", ut)


def graf_fordeling(rader):
    rader = sorted(rader, key=lambda r: r["andel_hoy_4_5"], reverse=True)
    fig, ax = plt.subplots(figsize=(11, 7))
    ys = range(len(rader))
    venstre = [0.0] * len(rader)
    for score_idx in range(5):
        andeler = [r["dist"][score_idx] / r["antall"] * 100 for r in rader]
        ax.barh(ys, andeler, left=venstre, color=SCORE_FARGE[score_idx],
                label=f"Score {score_idx + 1}", zorder=3, height=0.62)
        for i, (a, l) in enumerate(zip(andeler, venstre)):
            if a >= 6:
                ax.annotate(f"{a:.0f}%", (l + a / 2, i), ha="center",
                            va="center", fontsize=9,
                            color="white" if score_idx >= 3 else "#333")
        venstre = [l + a for l, a in zip(venstre, andeler)]

    etiketter = [f"{r['forkortelse']}  (n={r['antall']})" for r in rader]
    ax.set_yticks(list(ys))
    ax.set_yticklabels(etiketter, fontsize=11)
    ax.invert_yaxis()
    ax.set_xlim(0, 100)
    ax.set_xlabel("Andel av partiets løfter (%)", fontsize=11)
    ax.set_title("Fordeling av konkretiseringsgrad (score 1–5) per parti",
                 fontsize=16, fontweight="bold", loc="left", pad=16)
    ax.text(0, 1.02,
            "Mørkere farge = mer konkret/målbart løfte",
            transform=ax.transAxes, fontsize=10, color="#666")
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.spines["left"].set_color("#ccc")
    ax.spines["bottom"].set_color("#ccc")
    ax.tick_params(length=0)
    ax.legend(ncol=5, loc="upper center", bbox_to_anchor=(0.5, -0.08),
              frameon=False, fontsize=10)
    fig.subplots_adjust(left=0.16, bottom=0.14, top=0.86)
    ut = os.path.join(HER, "graf_fordeling_1_5.png")
    fig.savefig(ut, dpi=160, bbox_inches="tight")
    print("Lagret", ut)


if __name__ == "__main__":
    data = les_data()
    graf_snitt(data)
    graf_andel_hoy(data)
    graf_fordeling(data)
    print("Ferdig.")
