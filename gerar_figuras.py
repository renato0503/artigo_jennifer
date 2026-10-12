# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "matplotlib"]
# ///
"""Gerador de figuras reprodutíveis para o artigo O Silêncio das Rosas.

Uso:
    uv run gerar_figuras.py            # português -> dados/figuras/
    uv run gerar_figuras.py --lang en  # inglês    -> dados/figuras/en/
"""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

SEMENTE = 20261012
BASE = Path(__file__).resolve().parent
TINTA, DESTAQUE, ALERTA, CINZA, FAIXA = "#1a1a1a", "#1A365D", "#8c3b3b", "#8a8a8a", "#c9d4e3"

TXT = {
    "pt": {
        "categoria": "Categoria",
        "quantidade": "Número de falas",
        "fig1_distribuicao": "Distribuição das falas por categoria temática",
        "fig2_crencas": "Distribuição por crença central",
        "desvalor": "Desvalor",
        "desamparo": "Desamparo",
        "desamor": "Desamor",
        "naturalizacao": "Naturalização\nda violência",
        "ameaca": "Ameaça e\nintimidação",
        "humilhacao": "Humilhação e\ndesvalorização",
        "desvalorizacao": "Desvalorização\nemocional",
        "dependencia": "Dependência e\nvulnerabilidade",
        "controle": "Controle\ncoercitivo",
        "minimizacao": "Minimização\nda violência",
        "dep_emocional": "Dependência\nemocional",
        "autonomia": "Busca de\nautonomia",
        "total": "Total de falas",
        "fonte": "Fonte: Dados da pesquisa (2026).",
    },
    "en": {
        "categoria": "Category",
        "quantidade": "Number of statements",
        "fig1_distribuicao": "Distribution of statements by thematic category",
        "fig2_crencas": "Distribution by core belief",
        "desvalor": "Devaluation",
        "desamparo": "Helplessness",
        "desamor": "Lack of love",
        "naturalizacao": "Normalization\nof violence",
        "ameaca": "Threat and\nintimidation",
        "humilhacao": "Humiliation and\ndevaluation",
        "desvalorizacao": "Emotional\ndevaluation",
        "dependencia": "Dependency and\nvulnerability",
        "controle": "Coercive\ncontrol",
        "minimizacao": "Minimization of\nviolence",
        "dep_emocional": "Emotional\ndependency",
        "autonomia": "Search for\nautonomy",
        "total": "Total statements",
        "fonte": "Source: Research data (2026).",
    },
}


def estilo():
    plt.rcParams.update({
        "font.family": "serif",
        "font.serif": ["Times New Roman", "DejaVu Serif"],
        "font.size": 10,
        "axes.labelsize": 10,
        "axes.titlesize": 10.5,
        "axes.edgecolor": "#333333",
        "axes.linewidth": 0.8,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "legend.frameon": False,
        "svg.fonttype": "none",
        "figure.dpi": 100,
    })


def salvar(fig, nome: str, pasta: Path):
    pasta.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(pasta / f"{nome}.svg")
    fig.savefig(pasta / f"{nome}.png", dpi=300)
    plt.close(fig)
    print(f"ok: {pasta / nome}.svg/.png")


def fig1_distribuicao_categorias(t: dict, rng: np.random.Generator, pasta: Path):
    categorias = [
        t["naturalizacao"],
        t["ameaca"],
        t["humilhacao"],
        t["desvalorizacao"],
        t["dependencia"],
        t["controle"],
        t["minimizacao"],
        t["dep_emocional"],
        t["autonomia"],
    ]
    quantidades = [2, 8, 5, 26, 3, 5, 2, 2, 1]
    cores = [
        DESTAQUE, DESTAQUE, DESTAQUE, DESTAQUE,
        CINZA, CINZA, CINZA, CINZA, CINZA
    ]

    fig, ax = plt.subplots(figsize=(7.5, 4.0))
    bars = ax.bar(categorias, quantidades, color=cores, width=0.6, zorder=3)

    for bar in bars:
        height = bar.get_height()
        ax.annotate(f"{int(height)}",
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha="center", va="bottom",
                    fontsize=10, color=TINTA)

    ax.set_xlabel(t["categoria"], labelpad=8)
    ax.set_ylabel(t["quantidade"])
    ax.set_ylim(0, 30)
    ax.set_yticks(np.arange(0, 31, 5))
    ax.grid(axis="y", color=FAIXA, linewidth=0.5, zorder=0)
    ax.tick_params(axis="x", rotation=15)

    salvar(fig, "fig1_distribuicao_categorias", pasta)


def fig2_distribuicao_crencas(t: dict, rng: np.random.Generator, pasta: Path):
    crencas = [t["desvalor"], t["desamparo"], t["desamor"]]
    quantidades = [34, 16, 4]
    cores = [DESTAQUE, CINZA, ALERTA]

    fig, ax = plt.subplots(figsize=(5.0, 4.0))
    bars = ax.bar(crencas, quantidades, color=cores, width=0.5, zorder=3)

    for bar in bars:
        height = bar.get_height()
        ax.annotate(f"{int(height)}",
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha="center", va="bottom",
                    fontsize=11, color=TINTA)

    ax.set_xlabel(t["categoria"], labelpad=8)
    ax.set_ylabel(t["quantidade"])
    ax.set_ylim(0, 40)
    ax.set_yticks(np.arange(0, 41, 5))
    ax.grid(axis="y", color=FAIXA, linewidth=0.5, zorder=0)

    salvar(fig, "fig2_distribuicao_crencas", pasta)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lang", choices=["pt", "en"], default="pt")
    a = ap.parse_args()
    estilo()
    t = TXT[a.lang]
    pasta = BASE / "dados" / "figuras" / ("" if a.lang == "pt" else "en")
    for f in (fig1_distribuicao_categorias, fig2_distribuicao_crencas):
        f(t, np.random.default_rng(SEMENTE), pasta)


if __name__ == "__main__":
    main()
