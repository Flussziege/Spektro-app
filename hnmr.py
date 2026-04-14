"""
¹H-NMR-Simulator  –  regelbasiert mit Multiplizität
=====================================================
Benötigt: pip install rdkit numpy matplotlib

Aufruf:
    python nmr_1h_simulator.py                  # Ethanol (Standard)
    python nmr_1h_simulator.py "CC(=O)O"        # Essigsäure
    python nmr_1h_simulator.py "CCO"            # Ethanol
    python nmr_1h_simulator.py "CC(C)=O"        # Aceton
"""

import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from collections import defaultdict
from rdkit import Chem
from rdkit.Chem import AllChem

# ══════════════════════════════════════════════════════════════════════════════
#  SHIFT-INKREMENTE  (Shoolery-Regeln, erweitert)
#  Alle Werte in ppm; Basis = 0.23 ppm (TMS-Referenz)
# ══════════════════════════════════════════════════════════════════════════════

BASE_SHIFT_H = 0.23   # TMS-ähnliche Basis (für aliphatische CH)

# α-Inkremente: direkt am gleichen C-Atom gebundene Substituenten
# (Shoolery 1959 + Silverstein-Erweiterungen)
ALPHA_INCREMENTS_H = [
    ("[OX2H]",           2.56),   # –OH  (Alkohol)
    ("[OX2H0][#6]",      2.36),   # –OR  (Ether)
    ("[OX2][CX3]=O",     3.01),   # –OC(=O)R  (Ester-Sauerstoff-Seite)
    ("[CX3](=O)[OH]",    1.00),   # –COOH  (α zu Carbonyl, abgeschwächt)
    ("[CX3H0]=O",        1.20),   # –C(=O)R  (Keton/Aldehyd α)
    ("[CX3H1]=O",        1.20),   # Aldehyd α
    ("[F]",              4.00),   # –F
    ("[Cl]",             2.53),   # –Cl
    ("[Br]",             2.33),   # –Br
    ("[I]",              1.82),   # –I
    ("[NX3H2]",          1.57),   # –NH2
    ("[NX3H1]",          1.40),   # –NHR
    ("[NX3H0]",          1.20),   # –NR2
    ("[N+](=O)[O-]",     3.36),   # –NO2
    ("[SX2]",            1.11),   # –SR / –SH
    ("[CX2]#[NX1]",      1.20),   # –CN
    ("[cX3]",            1.85),   # Aryl (direkt)
    ("[CX3]=[CX3]",      0.80),   # Alkenyl α
    ("[CX2]#[CX2]",      0.65),   # Alkinyl α
    ("[CX4]",            0.50),   # sp3-C  (Shoolery C-Inkrement)
]

# β-Inkremente: 2 Bindungen vom H-tragenden C entfernt (abgeschwächt)
BETA_INCREMENTS_H = [
    ("[OX2H]",           0.33),
    ("[OX2H0][#6]",      0.40),
    ("[OX2][CX3]=O",     0.55),
    ("[CX3H0]=O",        0.20),
    ("[F]",              0.30),
    ("[Cl]",             0.42),
    ("[Br]",             0.36),
    ("[NX3H2]",          0.24),
    ("[N+](=O)[O-]",     0.50),
    ("[cX3]",            0.22),
    ("[CX4]",            0.18),
]

# Spezielle absolute Shifts für bestimmte Protonen-Typen
# Format: (SMARTS des H-tragenden Atoms, absoluter Shift)
# Das SMARTS matcht das C (oder Heteroatom), das das H trägt.
AROMATIC_H_SPECIAL_SHIFTS = [
    # ─────────────────────────────────────────────────────────────
    # Aromatische H relativ zu O-Substituenten (Phenol / Anisol / Arylether)
    # eher hochfeldverschoben
    # ─────────────────────────────────────────────────────────────
    ("[C4XH1]1c([OX2][#6])cccc1",         6.85),   # ortho zu OR
    ("[C4XH1]1cc([OX2][#6])ccc1",         6.95),   # meta zu OR
    ("[C4XH1]1ccc([OX2][#6])cc1",         6.90),   # para zu OR

    ("[C4XH1]1c([OX2H])cccc1",            6.80),   # ortho zu OH
    ("[C4XH1]1cc([OX2H])ccc1",            6.95),   # meta zu OH
    ("[C4XH1]1ccc([OX2H])cc1",            6.85),   # para zu OH

    # ─────────────────────────────────────────────────────────────
    # Aromatische H relativ zu Alkyl-Substituenten
    # leicht hochfeld
    # ─────────────────────────────────────────────────────────────
    ("[C4XH1]1c([CX4H3])cccc1",           7.10),   # ortho zu Ar-CH3
    ("[C4XH1]1cc([CX4H3])ccc1",           7.18),   # meta zu Ar-CH3
    ("[C4XH1]1ccc([CX4H3])cc1",           7.12),   # para zu Ar-CH3

    ("[C4XH1]1c([CH2][#6])cccc1",         7.12),   # ortho zu Ar-CH2R
    ("[C4XH1]1cc([CH2][#6])ccc1",         7.20),   # meta zu Ar-CH2R
    ("[C4XH1]1ccc([CH2][#6])cc1",         7.15),   # para zu Ar-CH2R

    # ─────────────────────────────────────────────────────────────
    # Aromatische H relativ zu Halogenen
    # moderat tieffeld
    # ─────────────────────────────────────────────────────────────
    ("[C4XH1]1c([F])cccc1",               7.00),   # ortho zu F
    ("[C4XH1]1cc([F])ccc1",               7.08),   # meta zu F
    ("[C4XH1]1ccc([F])cc1",               7.03),   # para zu F

    ("[C4XH1]1c([Cl])cccc1",              7.18),   # ortho zu Cl
    ("[C4XH1]1cc([Cl])ccc1",              7.24),   # meta zu Cl
    ("[C4XH1]1ccc([Cl])cc1",              7.20),   # para zu Cl

    ("[C4XH1]1c([Br])cccc1",              7.20),   # ortho zu Br
    ("[C4XH1]1cc([Br])ccc1",              7.25),   # meta zu Br
    ("[C4XH1]1ccc([Br])cc1",              7.21),   # para zu Br

    # ─────────────────────────────────────────────────────────────
    # Aromatische H relativ zu Nitro
    # deutlich tieffeld
    # ─────────────────────────────────────────────────────────────
    ("[C4XH1]1c([N+](=O)[O-])cccc1",      8.10),   # ortho zu NO2
    ("[C4XH1]1cc([N+](=O)[O-])ccc1",      7.65),   # meta zu NO2
    ("[C4XH1]1ccc([N+](=O)[O-])cc1",      7.85),   # para zu NO2

    # ─────────────────────────────────────────────────────────────
    # Aromatische H relativ zu Aldehyd
    # ─────────────────────────────────────────────────────────────
    ("[C4XH1]1c([CX3H1](=O))cccc1",       7.85),   # ortho zu CHO
    ("[C4XH1]1cc([CX3H1](=O))ccc1",       7.55),   # meta zu CHO
    ("[C4XH1]1ccc([CX3H1](=O))cc1",       7.75),   # para zu CHO

    # ─────────────────────────────────────────────────────────────
    # Aromatische H relativ zu Keton / Acyl
    # ─────────────────────────────────────────────────────────────
    ("[C4XH1]1c([CX3](=O)[#6])cccc1",     7.90),   # ortho zu COR
    ("[C4XH1]1cc([CX3](=O)[#6])ccc1",     7.55),   # meta zu COR
    ("[C4XH1]1ccc([CX3](=O)[#6])cc1",     7.78),   # para zu COR

    # ─────────────────────────────────────────────────────────────
    # Aromatische H relativ zu Ester / Carbonsäure
    # ─────────────────────────────────────────────────────────────
    ("[C4XH1]1c([CX3](=O)[OX2][#6])cccc1", 7.95),  # ortho zu COOR
    ("[C4XH1]1cc([CX3](=O)[OX2][#6])ccc1", 7.55),  # meta zu COOR
    ("[C4XH1]1ccc([CX3](=O)[OX2][#6])cc1", 7.85),  # para zu COOR

    ("[C4XH1]1c([CX3](=O)[OX2H])cccc1",   8.05),   # ortho zu COOH
    ("[C4XH1]1cc([CX3](=O)[OX2H])ccc1",   7.60),   # meta zu COOH
    ("[C4XH1]1ccc([CX3](=O)[OX2H])cc1",   7.90),   # para zu COOH

    # ─────────────────────────────────────────────────────────────
    # Aromatische H relativ zu Amino-Substituenten
    # eher hochfeld
    # ─────────────────────────────────────────────────────────────
    ("[C4XH1]1c([NX3])cccc1",             6.70),   # ortho zu NRx
    ("[C4XH1]1cc([NX3])ccc1",             7.00),   # meta zu NRx
    ("[C4XH1]1ccc([NX3])cc1",             6.80),   # para zu NRx
]

EXCHANGEABLE_H_SPECIAL_SHIFTS = [
    # ─────────────────────────────────────────────────────────────
    # Carbonsäure / stark H-gebundene OH
    # ─────────────────────────────────────────────────────────────
    ("[OX2H][CX3](=O)",                 11.50),  # COOH
    ("[OX2H]c[CX3H1](=O)",              10.80),  # o-Hydroxybenzaldehyd-artig
    ("[OX2H]c[CX3](=O)[OX2H]",          11.20),  # Salicylsäure-artig
    ("[OX2H]c[N+](=O)[O-]",             10.20),  # Nitrophenol-artig, stark deshielded

    # ─────────────────────────────────────────────────────────────
    # Phenole / aromatische OH
    # ─────────────────────────────────────────────────────────────
    ("[OX2H][c][NX3]",                   6.20),  # Aminophenol-artig, eher hochfeld
    ("[OX2H][c][OX2][#6]",               6.60),  # Methoxy-phenol / Guajacol-artig
    ("[OX2H][c]",                        7.20),  # allgemeines Phenol-OH

    # ─────────────────────────────────────────────────────────────
    # Enol-/vinyloges OH / Heteroaromat-OH
    # ─────────────────────────────────────────────────────────────
    ("[OX2H][CX3]=[CX3]",                9.50),  # enolisches OH
    ("[OX2H][c]1ccccn1",                 9.80),  # Hydroxy-pyridin/quinolin-artig grob
    ("[OX2H][c]1cccc[c,n]1",             9.20),  # heteroaromatisches OH, grob

    # ─────────────────────────────────────────────────────────────
    # Alkohole
    # ─────────────────────────────────────────────────────────────
    ("[OX2H][CH]([c])",                  2.90),  # benzylicher sekundärer Alkohol
    ("[OX2H][CH2][c]",                   2.70),  # Benzylalkohol-OH
    ("[OX2H][CX4]",                      2.50),  # allgemeiner Alkohol
    ("[OX2H][CX4][OX2][#6]",             3.20),  # OH in O-reicher Umgebung (Acetal/Hemiacetal grob)

    # ─────────────────────────────────────────────────────────────
    # Amid / Carbamat / Harnstoff / Sulfonamid
    # ─────────────────────────────────────────────────────────────
    ("[NX3H2][CX3](=O)",                 7.60),  # primäres Amid NH2
    ("[NX3H1][CX3](=O)",                 7.80),  # sekundäres Amid NH
    ("[NX3H1]C(=O)O",                    6.80),  # Carbamat/Urethan NH
    ("[NX3H1]S(=O)(=O)",                 7.90),  # Sulfonamid NH
    ("[NX3H1]C(=O)N",                    6.20),  # Harnstoff-/Urea-artig
    ("[NX3H2]C(=O)N",                    5.90),  # primäres Harnstoff-NH2

    # ─────────────────────────────────────────────────────────────
    # Arylamine / Aniline
    # ─────────────────────────────────────────────────────────────
    ("[NX3H2][c]",                       3.80),  # Anilin-NH2
    ("[NX3H1][c]",                       4.20),  # Arylamin-NH
    ("[NX3H2][c][N+](=O)[O-]",           5.20),  # Nitroanilin-artig, stärker tieffeld
    ("[NX3H2][c][OX2][#6]",              3.40),  # Anisidin-artig
    ("[NX3H2][c][OX2H]",                 4.30),  # Aminophenol-artig

    # ─────────────────────────────────────────────────────────────
    # Heteroaromatische NH
    # ─────────────────────────────────────────────────────────────
    ("[nH]1cccc1",                      10.20),  # Pyrrol-NH
    ("[nH]1cccc2ccccc12",              10.60),  # Indol-NH
    ("[nH]1ccnc1",                     11.20),  # Imidazol/Pyrazol-artig grob
    ("[nH]",                           10.00),  # allgemeines aromatisches NH

    # ─────────────────────────────────────────────────────────────
    # Imine / Oxime / Hydroxylamine (grob)
    # ─────────────────────────────────────────────────────────────
    ("[NX3H][CX3]=[NX2]",               8.20),  # amidin-/imine-NH grob
    ("[OX2H][NX2]=[CX3]",              10.50),  # Oxime OH grob
    ("[NX3H][OX2][#6]",                 5.20),  # Hydroxylamin-artig NH grob

    # ─────────────────────────────────────────────────────────────
    # Thiol
    # ─────────────────────────────────────────────────────────────
    ("[SX2H][c]",                       3.20),  # Thiophenol-artig SH
    ("[SX2H]",                          1.80),  # allgemeines Thiol-SH
]


SPECIAL_H_SHIFTS = [

    # stark spezifische austauschbare Protonen zuerst
    *EXCHANGEABLE_H_SPECIAL_SHIFTS,

    # ─────────────────────────────────────────────────────────────
    # Sehr charakteristische Heteroatom-/Carbonyl-Protonen
    # ─────────────────────────────────────────────────────────────
    ("[CX3H1](=O)",                     9.50),   # Aldehyd-H
    ("[CX3H2](=O)",                     9.60),   # Aldehyd-H für Formaldehyd
    ("[OX2H][CX3](=O)",               11.50),   # Carbonsäure-OH
    ("[OX2H][c]",                      7.20),   # Phenol-OH
    ("[CX2H1]#[CX2]",                  2.50),   # terminales Alkin-H

    # ─────────────────────────────────────────────────────────────
    # O-gebundene Alkylprotonen
    # ─────────────────────────────────────────────────────────────
    ("[CH3][OX2][CX3](=O)",            3.75),   # Ester-OCH3
    ("[CH2][OX2][CX3](=O)",            4.15),   # Ester-OCH2
    ("[CX4H1]([OX2][CX3](=O))",        5.00),   # O-CH in Ester-/Carbonat-ähnlicher Umgebung

    ("[CH3][OX2][c]",                  3.75),   # Anisol-artiges OCH3
    ("[CH2][OX2][c]",                  4.25),   # Ar-OCH2
    ("[CH1]([OX2][c])",                4.80),   # Ar-OCH

    ("[CH3][OX2][#6]",                 3.35),   # allgemeines OCH3
    ("[CH2][OX2][#6]",                 3.55),   # allgemeines OCH2
    ("[CX4H1][OX2][#6]",               3.90),   # allgemeines OCH

    # ─────────────────────────────────────────────────────────────
    # N-gebundene Alkylprotonen
    # ─────────────────────────────────────────────────────────────
    ("[CH3][NX3][CX3](=O)",            3.00),   # N-CH3 in Amid
    ("[CH2][NX3][CX3](=O)",            3.30),   # N-CH2 in Amid

    ("[CH3][NX3]",                     2.30),   # N-CH3 (Amin)
    ("[CH2][NX3]",                     2.60),   # N-CH2 (Amin)
    ("[CX4H1][NX3]",                   3.00),   # N-CH (Amin)

    # ─────────────────────────────────────────────────────────────
    # α zum Carbonyl
    # ─────────────────────────────────────────────────────────────
    ("[CH3][CX3](=O)[#6]",             2.10),   # Methylketon
    ("[CH3][CX3H1](=O)",               2.20),   # CH3-CHO
    ("[CH2][CX3](=O)",                 2.35),   # CH2 alpha zu C=O
    ("[CX4H1][CX3](=O)",               2.55),   # CH alpha zu C=O

    # ─────────────────────────────────────────────────────────────
    # Benzylich
    # ────────────────────────────────────────────────────────────

    # benzylich + Heteroatom am selben C
    ("[CH2]([OX2H])[c]",               4.60),   # Benzylalkohol CH2OH
    ("[CH2]([OX2][#6])[c]",            4.45),   # Benzyl-OR
    ("[CH2]([NX3])[c]",                3.75),   # Benzylamin-artig

    
    # allgemeine benzyliche Protonen
    ("[CH3][c]",                       2.30),   # Ar-CH3
    ("[CH2][c]",                       2.75),   # Ar-CH2
    ("[CX4H1][c]",                     3.10),   # Ar-CH

    # ─────────────────────────────────────────────────────────────
    # Allylisch / propargylisch
    # ─────────────────────────────────────────────────────────────
    ("[CH3][CX3]=[CX3]",               1.75),   # allylisches CH3
    ("[CH2][CX3]=[CX3]",               2.00),   # allylisches CH2
    ("[CX4H1][CX3]=[CX3]",             2.20),   # allylisches CH

    ("[CH3][CX2]#[CX2]",               1.90),   # propargylisches CH3
    ("[CH2][CX2]#[CX2]",               2.20),   # propargylisches CH2
    ("[CX4H1][CX2]#[CX2]",             2.45),   # propargylisches CH

    # ─────────────────────────────────────────────────────────────
    # α zu Nitril / Nitro / Halogen
    # ─────────────────────────────────────────────────────────────
    ("[CH3][CX2]#[NX1]",               2.05),   # CH3-CN
    ("[CH2][CX2]#[NX1]",               2.35),   # CH2-CN
    ("[CX4H1][CX2]#[NX1]",             2.60),   # CH-CN

    ("[CH3][N+](=O)[O-]",              4.30),   # Nitroalkan CH3
    ("[CH2][N+](=O)[O-]",              4.45),   # Nitroalkan CH2
    ("[CX4H1][N+](=O)[O-]",            4.70),   # Nitroalkan CH

    # Halogenierte CH
    ("[CH3][F]",                       4.10),
    ("[CH2][F]",                       4.35),
    ("[CX4H1][F]",                     4.70),

    ("[CH3][Cl]",                      3.05),
    ("[CH2][Cl]",                      3.45),
    ("[CX4H1][Cl]",                    4.00),

    ("[CH3][Br]",                      2.70),
    ("[CH2][Br]",                      3.30),
    ("[CX4H1][Br]",                    3.85),

    ("[CH3][I]",                       2.20),
    ("[CH2][I]",                       3.15),
    ("[CX4H1][I]",                     3.60),

    # ─────────────────────────────────────────────────────────────
    # Acetal-/Ketal-artige Zentren
    # ─────────────────────────────────────────────────────────────
    ("[CX4H1]([OX2][#6])([OX2][#6])",  4.85),   # Acetal-CH
    ("[CH2]([OX2][#6])[OX2][#6]",      4.20),   # Acetal-CH2
    ("[CX4H1]([OX2H])([OX2][#6])",     4.60),   # Hemiacetal-CH

    # Aromatische Spezialfälle VOR der allgemeinen Aromaten-Regel
    *AROMATIC_H_SPECIAL_SHIFTS,

    # ─────────────────────────────────────────────────────────────
    # Alken-Protonen
    # ─────────────────────────────────────────────────────────────
    ("[CX3H2]=[CX3]",                  5.10),   # terminales =CH2
    ("[CX3H1]=[CX3]",                  5.50),   # internes =CH

    # ─────────────────────────────────────────────────────────────
    # Allgemeines, schön weit nach unten
    # ─────────────────────────────────────────────────────────────

    ("[OX2H][CX4]",                    2.50),   # Alkohol-OH
    ("[SX2H]",                         1.80),   # Thiol-SH
    ("[NX3H2][CX4]",                   1.60),   # prim. Amin-NH2
    ("[NX3H][CX3](=O)",                7.80),   # Amid-NH

    # ─────────────────────────────────────────────────────────────
    # Aromatische Protonen
    # ─────────────────────────────────────────────────────────────
    ("[cH]",                           7.27),   # allgemeines Ar-H
]


# ══════════════════════════════════════════════════════════════════════════════
#  KOPPLUNGSKONSTANTEN  (J in Hz, typische Werte)
# ══════════════════════════════════════════════════════════════════════════════

# Vicinal (3J, H-C-C-H): Standardwert 7.0 Hz
# Geminal (2J, H-C-H):   für CH2 ~12 Hz, meist nicht sichtbar wenn äquivalent
# Allylisch (4J):        ~1.5 Hz
# Aromatisch ortho (3J): ~8 Hz, meta (4J): ~2 Hz

J_VICINAL         = 7.0    # Hz  (sp3-sp3, Alkyl)
J_GEMINAL         = 12.0   # Hz  (2J, nur grob vorbereitet)
J_ALLYLIC         = 1.5    # Hz  (4J, allylisch)
J_AR_ORTHO        = 8.0    # Hz
J_AR_META         = 2.0    # Hz

J_VINYL_TRANS     = 16.0   # Hz  trans-CH=CH
J_VINYL_CIS       = 10.0   # Hz  cis-CH=CH
J_VINYL_GEMINAL   = 2.0    # Hz  =CH2 geminal / terminal-vinylic klein
J_VINYL_UNDEF     = 12.0   # Hz  wenn E/Z nicht spezifiziert

J_ALDEHYDE_ALPHA  = 2.2    # Hz  CHO zu alpha-CH
SPECTROMETER      = 400.0  # MHz


# ══════════════════════════════════════════════════════════════════════════════
#  HILFSFUNKTIONEN
# ══════════════════════════════════════════════════════════════════════════════


def update_nmr_x_ticks(ax):
    x0, x1 = ax.get_xlim()
    span = abs(x1 - x0)

    # sinnvolle Major-Schritte je nach Zoomstufe
    if span > 20:
        major = 2.0
    elif span > 10:
        major = 1.0
    elif span > 5:
        major = 0.5
    elif span > 2:
        major = 0.2
    elif span > 1:
        major = 0.1
    elif span > 0.5:
        major = 0.05
    else:
        major = 0.02

    minor = major / 4

    ax.xaxis.set_major_locator(ticker.MultipleLocator(major))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(minor))

    # hübsches Zahlenformat
    if major >= 1:
        ax.xaxis.set_major_formatter(ticker.FormatStrFormatter("%.0f"))
    elif major >= 0.1:
        ax.xaxis.set_major_formatter(ticker.FormatStrFormatter("%.1f"))
    else:
        ax.xaxis.set_major_formatter(ticker.FormatStrFormatter("%.2f"))

def pascal_row(n: int) -> list[int]:
    """Gibt die n-te Zeile des Pascalschen Dreiecks zurück (0-indiziert)."""
    row = [1]
    for k in range(1, n + 1):
        row.append(row[-1] * (n - k + 1) // k)
    return row


def convolve_multiplets(groups: list[tuple[int, float]]) -> list[tuple[float, float]]:
    """
    Kombiniert mehrere Kopplungsgruppen zu einem zusammengesetzten Multiplett.

    groups: Liste von (n_coupling_H, J_hz)
            z.B. [(2, 7.0), (1, 2.0)] → Dublett von Tripletts

    Gibt Liste von (relative_offset_ppm, relative_intensity) zurück.
    """
    lines = [(0.0, 1.0)]   # Start: eine Linie bei 0

    for n_h, j_hz in groups:
        if n_h == 0:
            continue
        j_ppm = j_hz / SPECTROMETER
        pascal = pascal_row(n_h)
        new_lines = []
        offsets = [(-n_h / 2 + k) * j_ppm for k in range(n_h + 1)]

        for base_offset, base_intens in lines:
            for dp, p_intens in zip(offsets, pascal):
                new_lines.append((base_offset + dp, base_intens * p_intens))

        # Linien zusammenführen, die sehr nah beieinander liegen
        merged = {}
        for offset, intens in new_lines:
            key = round(offset, 6)
            merged[key] = merged.get(key, 0.0) + intens
        lines = list(merged.items())

    # Normieren auf max = 1
    max_i = max(i for _, i in lines)
    return [(o, i / max_i) for o, i in lines]


def get_equivalent_rank(mol) -> dict[int, int]:
    """Gibt Morgan-Äquivalenzrang für alle Atome zurück."""
    return dict(enumerate(Chem.CanonicalRankAtoms(mol, breakTies=False)))

def count_attached_explicit_h(atom) -> int:
    """Zählt explizite H-Atome, die direkt an atom gebunden sind."""
    return sum(1 for nb in atom.GetNeighbors() if nb.GetAtomicNum() == 1)


def get_carbon_neighbors(atom):
    """Nur direkt gebundene C-Nachbarn."""
    return [nb for nb in atom.GetNeighbors() if nb.GetAtomicNum() == 6]


def get_bond_between(mol, a_idx: int, b_idx: int):
    return mol.GetBondBetweenAtoms(a_idx, b_idx)


def is_aldehydic_carbon(atom) -> bool:
    """True für das C des Formylprotons: [CX3H1](=O)"""
    if atom.GetAtomicNum() != 6:
        return False
    if count_attached_explicit_h(atom) != 1:
        return False

    for bond in atom.GetBonds():
        if bond.GetBondTypeAsDouble() == 2.0:
            other = bond.GetOtherAtom(atom)
            if other.GetAtomicNum() == 8:
                return True
    return False


def is_vinylic_carbon(atom) -> bool:
    """sp2-C mit mindestens einem H und C=C-Bindung zu C."""
    if atom.GetAtomicNum() != 6:
        return False
    if count_attached_explicit_h(atom) < 1:
        return False

    for bond in atom.GetBonds():
        if bond.GetBondTypeAsDouble() == 2.0:
            other = bond.GetOtherAtom(atom)
            if other.GetAtomicNum() == 6:
                return True
    return False


def get_vinylic_partner(atom):
    """Gibt den gegenüberliegenden C-Partner der C=C-Bindung zurück."""
    for bond in atom.GetBonds():
        if bond.GetBondTypeAsDouble() == 2.0:
            other = bond.GetOtherAtom(atom)
            if other.GetAtomicNum() == 6:
                return other, bond
    return None, None


def get_double_bond_stereo_j(bond) -> float:
    """
    Nutzt RDKit-Stereoinfo der Doppelbindung.
    Funktioniert nur, wenn der SMILES E/Z-Stereo enthält.
    """
    stereo = bond.GetStereo()
    if stereo == Chem.rdchem.BondStereo.STEREOE:
        return J_VINYL_TRANS
    if stereo == Chem.rdchem.BondStereo.STEREOZ:
        return J_VINYL_CIS
    return J_VINYL_UNDEF


# ══════════════════════════════════════════════════════════════════════════════
#  SHIFT-BERECHNUNG FÜR EIN H
# ══════════════════════════════════════════════════════════════════════════════

def _neighbors_at_dist(mol, idx: int, dist: int) -> list[int]:
    visited, frontier = {idx}, {idx}
    for _ in range(dist):
        nxt = set()
        for i in frontier:
            for nb in mol.GetAtomWithIdx(i).GetNeighbors():
                if nb.GetIdx() not in visited:
                    nxt.add(nb.GetIdx())
        visited |= nxt
        frontier = nxt
    return list(frontier)


def calculate_h_shift(heavy_atom_idx: int, mol) -> float:
    """
    Berechnet den ¹H-Shift für ein H, das an heavy_atom_idx gebunden ist.
    Gibt einen Shift in ppm zurück.
    """
    # 1. Spezielle absolute Shifts haben Vorrang
    for smarts, absolute_shift in SPECIAL_H_SHIFTS:
        patt = Chem.MolFromSmarts(smarts)
        if patt is None:
            continue
        for match in mol.GetSubstructMatches(patt):
            if match[0] == heavy_atom_idx:
                return absolute_shift

    # 2. Regelbasierte Inkrementberechnung (Shoolery)
    shift = BASE_SHIFT_H

    alpha_nb = _neighbors_at_dist(mol, heavy_atom_idx, 1)
    beta_nb  = _neighbors_at_dist(mol, heavy_atom_idx, 2)

    def apply_inc(neighbor_list, table):
        total = 0.0
        for nb_idx in neighbor_list:
            for smarts, value in table:
                patt = Chem.MolFromSmarts(smarts)
                if patt is None:
                    continue
                for match in mol.GetSubstructMatches(patt):
                    if match[0] == nb_idx:
                        total += value
                        break
        return total

    shift += apply_inc(alpha_nb, ALPHA_INCREMENTS_H)
    shift += apply_inc(beta_nb,  BETA_INCREMENTS_H)

    return shift


# ══════════════════════════════════════════════════════════════════════════════
#  MULTIPLIZITÄT: Zählen der koppelnden H-Nachbarn
# ══════════════════════════════════════════════════════════════════════════════

def get_coupling_groups(heavy_atom_idx: int, mol, equiv_ranks: dict) -> list[tuple[int, float]]:
    """
    Bestimmt Kopplungsgruppen für ein Proton an heavy_atom_idx.

    Rückgabe:
        Liste von (n_äquivalente_H, J_hz)
    """
    atom = mol.GetAtomWithIdx(heavy_atom_idx)

    # Austauschbare Protonen koppeln hier nicht
    if atom.GetAtomicNum() in (8, 16):   # O, S
        return []
    if atom.GetAtomicNum() == 7:         # N
        return []

    # ─────────────────────────────────────────────────────────────
    # Aromatische Protonen
    # ─────────────────────────────────────────────────────────────
    if atom.GetIsAromatic():
        coupling = []
        ortho_ranks = defaultdict(int)
        meta_ranks = defaultdict(int)

        aromatic_neighbors = [nb for nb in atom.GetNeighbors() if nb.GetIsAromatic()]

        # ortho
        for nb in aromatic_neighbors:
            h_count = count_attached_explicit_h(nb)
            if h_count > 0:
                ortho_ranks[equiv_ranks[nb.GetIdx()]] += h_count

        # meta
        for nb in aromatic_neighbors:
            for nb2 in nb.GetNeighbors():
                if nb2.GetIdx() == heavy_atom_idx:
                    continue
                if not nb2.GetIsAromatic():
                    continue
                if nb2 in aromatic_neighbors:
                    continue  # verhindert ortho-Doppelzählung
                h_count = count_attached_explicit_h(nb2)
                if h_count > 0:
                    meta_ranks[equiv_ranks[nb2.GetIdx()]] += h_count

        for _, n in ortho_ranks.items():
            coupling.append((n, J_AR_ORTHO))
        for _, n in meta_ranks.items():
            coupling.append((n, J_AR_META))

        return coupling

    # ─────────────────────────────────────────────────────────────
    # Aldehydproton: kleine 3J-Kopplung zu alpha-CH
    # ─────────────────────────────────────────────────────────────
    if is_aldehydic_carbon(atom):
        coupling = []
        rank_to_nh = defaultdict(int)

        for nb in get_carbon_neighbors(atom):
            # nur einfach gebundener alpha-C, nicht Carbonyl-O
            bond = get_bond_between(mol, atom.GetIdx(), nb.GetIdx())
            if bond is None or bond.GetBondTypeAsDouble() != 1.0:
                continue

            n_h = count_attached_explicit_h(nb)
            if n_h > 0:
                rank_to_nh[equiv_ranks[nb.GetIdx()]] += n_h

        for _, n in rank_to_nh.items():
            coupling.append((n, J_ALDEHYDE_ALPHA))

        return coupling

    # ─────────────────────────────────────────────────────────────
    # Vinyliche Protonen: cis/trans über Doppelbindung
    # ─────────────────────────────────────────────────────────────
    if is_vinylic_carbon(atom):
        coupling = []
        partner, dbond = get_vinylic_partner(atom)

        # 3J über C=C
        if partner is not None:
            partner_h = count_attached_explicit_h(partner)
            this_h = count_attached_explicit_h(atom)

            if partner_h > 0:
                # internes CH=CH
                if this_h == 1 and partner_h == 1:
                    coupling.append((1, get_double_bond_stereo_j(dbond)))
                # terminales =CH2 gegen CH
                elif this_h == 2 and partner_h == 1:
                    coupling.append((1, J_VINYL_UNDEF))
                # terminales =CH2 gegen =CH2
                elif this_h == 1 and partner_h == 2:
                    coupling.append((2, J_VINYL_UNDEF))
                # grober Fallback
                else:
                    coupling.append((partner_h, J_VINYL_UNDEF))

            # geminale Kopplung auf =CH2 grob als kleines Dublett
            if this_h == 2:
                coupling.append((1, J_VINYL_GEMINAL))

        # allylische 4J-Kopplung
        rank_to_allylic_h = defaultdict(int)

        for nb in get_carbon_neighbors(atom):
            bond = get_bond_between(mol, atom.GetIdx(), nb.GetIdx())
            if bond is None:
                continue

            # nur sigma-Nachbarn, nicht der C=C-Partner selbst
            if bond.GetBondTypeAsDouble() != 1.0:
                continue

            n_h = count_attached_explicit_h(nb)
            if n_h > 0:
                rank_to_allylic_h[equiv_ranks[nb.GetIdx()]] += n_h

        for _, n in rank_to_allylic_h.items():
            coupling.append((n, J_ALLYLIC))

        return coupling

    # ─────────────────────────────────────────────────────────────
    # Normale aliphatische / nicht-aromatische / nicht-vinyliche C-H
    # ─────────────────────────────────────────────────────────────
    rank_to_nh = defaultdict(int)

    for neighbor_c in get_carbon_neighbors(atom):
        bond = get_bond_between(mol, atom.GetIdx(), neighbor_c.GetIdx())
        if bond is None:
            continue

        # normale vicinale Kopplung nur über Einfachbindung
        if bond.GetBondTypeAsDouble() != 1.0:
            continue

        n_h = count_attached_explicit_h(neighbor_c)
        if n_h > 0:
            rank_to_nh[equiv_ranks[neighbor_c.GetIdx()]] += n_h

    coupling = [(n, J_VICINAL) for n in rank_to_nh.values() if n > 0]

    # allylische 4J-Kopplung
    for nb in atom.GetNeighbors():
        if nb.GetAtomicNum() != 6:
            continue

        for bond in nb.GetBonds():
            if bond.GetBondTypeAsDouble() == 2.0:
                other = bond.GetOtherAtom(nb)
                if other.GetAtomicNum() == 6 and other.GetIdx() != atom.GetIdx():
                    n_h_allylic = count_attached_explicit_h(other)
                    if n_h_allylic > 0:
                        coupling.append((n_h_allylic, J_ALLYLIC))

    return coupling


# ══════════════════════════════════════════════════════════════════════════════
#  HAUPTFUNKTION: PEAKS BERECHNEN
# ══════════════════════════════════════════════════════════════════════════════

def compute_1h_peaks(smiles: str, seed: int = None
                     ) -> list[dict]:
    """
    Berechnet alle ¹H-NMR Peaks für ein Molekül.

    Gibt eine Liste von Dicts zurück:
        {
          "shift":        float   (ppm, Zentrums-Shift),
          "n_h":          int     (Anzahl äquivalenter H),
          "multiplet":    list[(offset_ppm, rel_intensity)],
          "label":        str     (z.B. "CH3", "OH"),
          "atom_idx":     int     (Schweratomindex des repräsentativen H-Trägers),
        }
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError(f"Ungültiger SMILES: {smiles}")
    mol = Chem.AddHs(mol)

    rng = np.random.default_rng(
        seed if seed is not None else sum(ord(c) for c in smiles)
    )

    equiv_ranks = get_equivalent_rank(mol)

    rank_to_atoms: dict[int, list[int]] = defaultdict(list)

    for atom in mol.GetAtoms():
        if atom.GetAtomicNum() == 1:
            continue

        n_h = count_attached_explicit_h(atom)
        if n_h == 0:
            continue

        r = equiv_ranks[atom.GetIdx()]
        rank_to_atoms[r].append(atom.GetIdx())

    peaks = []

    for heavy_rank, heavy_indices in rank_to_atoms.items():
        rep_idx = heavy_indices[0]
        rep_atom = mol.GetAtomWithIdx(rep_idx)

        n_h = sum(count_attached_explicit_h(mol.GetAtomWithIdx(idx)) for idx in heavy_indices)

        # Shift berechnen
        base_shift = calculate_h_shift(rep_idx, mol)
        shift = base_shift + rng.normal(0, 0.03)   # minimales Rauschen

        # Kopplungsgruppen bestimmen
        coupling_groups = get_coupling_groups(rep_idx, mol, equiv_ranks)

        # Multiplettlinien berechnen
        multiplet = convolve_multiplets(coupling_groups)

        # Atomsymbol für Label
        sym = rep_atom.GetSymbol()
        h_label = f"{sym}H{n_h}" if n_h > 1 else f"{sym}H"
        # Multiplizitätsbezeichnung
        total_n = sum(n for n, _ in coupling_groups)
        mult_names = {0: "s", 1: "d", 2: "t", 3: "q", 4: "quint",
                      5: "sext", 6: "sept"}
        mult_str = mult_names.get(total_n, f"m({total_n+1})")
        if len(coupling_groups) > 1:
            mult_str = "dd" if total_n == 2 else f"m"

        peaks.append({
            "shift":     float(shift),
            "n_h":       n_h,
            "multiplet": multiplet,
            "label":     h_label,
            "mult_str":  mult_str,
            "atom_idx":  rep_idx,
        })

    # Nach Shift sortieren (Hochfeld → Tieffeld)
    peaks.sort(key=lambda p: p["shift"])
    return peaks


# ══════════════════════════════════════════════════════════════════════════════
#  SPEKTRUM SYNTHETISIEREN
# ══════════════════════════════════════════════════════════════════════════════

def synthesize_1h_spectrum(peaks: list[dict],
                            ppm_range: tuple = (-0.5, 14.0),
                            n_points: int = 8000,
                            line_width_ppm: float = 0.008,
                            noise_level: float = 0.003) -> tuple[np.ndarray, np.ndarray]:
    """
    Synthetisiert das ¹H-NMR-Spektrum aus den berechneten Peaks.
    Jede Multiplett-Linie wird als Lorentz-Profil dargestellt.
    """
    ppm_axis = np.linspace(ppm_range[1], ppm_range[0], n_points)
    spectrum  = np.zeros(n_points)

    for peak in peaks:
        center  = peak["shift"]
        n_h     = peak["n_h"]
        for offset, rel_intens in peak["multiplet"]:
            pos = center + offset
            # Lorentz-Profil: realistischer für NMR als Gauß
            lorentz = 1.0 / (1.0 + ((ppm_axis - pos) / (line_width_ppm / 2))**2)
            spectrum += n_h * rel_intens * lorentz



    # Schwaches Rauschen
    rng = np.random.default_rng(42)
    spectrum += rng.normal(0, noise_level, n_points)
    spectrum = np.clip(spectrum, 0, None)

    return ppm_axis, spectrum


# ══════════════════════════════════════════════════════════════════════════════
#  VISUALISIERUNG
# ══════════════════════════════════════════════════════════════════════════════

def plot_1h_nmr(ppm_axis: np.ndarray, spectrum: np.ndarray,
                peaks: list[dict], smiles: str,
                show_integrals: bool = True, show_title: bool = True) -> plt.Figure:

    fig, ax = plt.subplots(figsize=(13, 5.5), facecolor="#fafaf8")
    ax.set_facecolor("#fafaf8")

    # ── Spektrumslinie ────────────────────────────────────────────────────────
    ax.plot(ppm_axis, spectrum, color="#1a4f8a", linewidth=1.0, zorder=4)
    ax.fill_between(ppm_axis, spectrum, 0, alpha=0.06, color="#1a4f8a", zorder=2)

    # ── Integrallinie ─────────────────────────────────────────────────────────
    spec_max = float(np.max(spectrum)) if len(spectrum) else 1.0
    max_nh = max(p["n_h"] for p in peaks) if peaks else 1.0

    integral_max = 0.0

    if show_integrals:
        integral_y = np.zeros_like(spectrum)
        dx = abs(ppm_axis[1] - ppm_axis[0])

        for peak in peaks:
            mask = np.abs(ppm_axis - peak["shift"]) < 0.30
            region = spectrum.copy()
            region[~mask] = 0

            local_int = np.cumsum(region) * dx

            start = np.argmax(mask)
            end   = len(mask) - np.argmax(mask[::-1]) - 1

            if end > start:
                integral_y[start:end] += local_int[start:end] - local_int[start]
                integral_y[end:] += integral_y[end - 1]

        if integral_y.max() > 0:
            integral_scaled = integral_y / integral_y.max() * max_nh
            integral_scaled = integral_scaled + 0.05 * (max_nh + 1)

            ax.step(ppm_axis, integral_scaled,
                    where='mid',
                    color="#c04010",
                    linewidth=1.2,
                    alpha=0.8,
                    zorder=5)

            integral_max = float(np.max(integral_scaled))

    # dynamische Obergrenze aus echtem Spektrum + Integral
    y_top = max(spec_max, integral_max, max_nh) * 1.22 + 0.15

    # ── Peak-Beschriftungen ───────────────────────────────────────────────────
    if show_title:
        placed_labels = []
        for peak in sorted(peaks, key=lambda p: -p["n_h"]):
            x = peak["shift"]

            mask = np.abs(ppm_axis - x) < 0.20
            if not mask.any():
                continue

            y_max = spectrum[mask].max()
            y_label = y_max + 0.08

            too_close = any(abs(px - x) < 0.25 and abs(py - y_label) < 0.08
                            for px, py in placed_labels)
            if too_close:
                y_label += 0.10

            placed_labels.append((x, y_label))

            ax.text(x, y_label,
                    f"{peak['shift']:.2f}\n{peak['mult_str']}, {peak['n_h']}H",
                    ha="center", va="bottom", fontsize=7.5,
                    color="#7a3a00", zorder=6,
                    bbox=dict(boxstyle="round,pad=0.15", fc="#faf5ee",
                            ec="#ddbb88", linewidth=0.5, alpha=0.85))

    # ── Achsen ────────────────────────────────────────────────────────────────
    total_h = sum(p["n_h"] for p in peaks)

    ax.set_xlim(12.5, -0.3)
    ax.set_ylim(0, y_top)

    ax.set_xlabel("Chemical Shift δ (ppm)", fontsize=11)
    ax.set_ylabel("Protonenzahl (rel. Intensität)", fontsize=10)

    update_nmr_x_ticks(ax)

    ax.yaxis.set_major_locator(ticker.MultipleLocator(1.0))
    ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.5))

    ax.grid(True, which="major", color="#cccccc", linewidth=0.5)
    ax.grid(True, which="minor", color="#e8e8e8", linewidth=0.3)

    def _on_xlim_changed(event_ax):
        update_nmr_x_ticks(event_ax)
        event_ax.figure.canvas.draw_idle()

    ax.callbacks.connect("xlim_changed", _on_xlim_changed)

    for spine in ["top", "right", "left"]:
        ax.spines[spine].set_visible(False)
    ax.spines["bottom"].set_color("#888888")

    ax.tick_params(labelsize=9)
    ax.axvline(12.5, color="#444444", linewidth=1.2)

    if show_title:
        fig.suptitle(
            f"Simuliertes ¹H-NMR-Spektrum (400 MHz, CDCl₃)    SMILES: {smiles}",
            fontsize=11, color="#333333"
        )
    else:
        fig.suptitle(
            f"Simuliertes ¹H-NMR-Spektrum (400 MHz, CDCl₃)",
            fontsize=11, color="#333333"
        )

    fig.tight_layout()
    return fig


# ══════════════════════════════════════════════════════════════════════════════
#  KONSOLENAUSGABE
# ══════════════════════════════════════════════════════════════════════════════

def print_peak_table(peaks: list[dict], smiles: str):
    mult_full = {"s": "Singulett", "d": "Dublett", "t": "Triplett",
                 "q": "Quartett", "dd": "Dublett v. Dublett",
                 "quint": "Quintett", "sext": "Sextett", "sept": "Septett"}
    print(f"\n{'═'*60}")
    print(f"  ¹H-NMR  |  {smiles}")
    print(f"{'═'*60}")
    print(f"  {'δ (ppm)':<10} {'Mult.':<8} {'nH':<5} {'Linien':<8} Gruppe")
    print(f"  {'─'*55}")
    for p in sorted(peaks, key=lambda x: -x["shift"]):
        n_lines = len(p["multiplet"])
        full    = mult_full.get(p["mult_str"], p["mult_str"])
        print(f"  {p['shift']:<10.2f} {p['mult_str']:<8} {p['n_h']:<5} {n_lines:<8} {p['label']}  ({full})")
    print(f"{'═'*60}\n")


# ══════════════════════════════════════════════════════════════════════════════
#  HAUPT-API
# ══════════════════════════════════════════════════════════════════════════════

def simulate_1h_nmr(smiles: str,
                    seed: int = 42,
                    plot: bool = True,
                    verbose: bool = True,
                    line_width: float = 0.008,
                    show_integrals: bool = True,
                    show_title: bool = True, 
                    testrun: bool = False):
    """
    Vollständige Pipeline: SMILES → ¹H-NMR Spektrum.

    Returns dict mit:
        "peaks"         – berechnete Peak-Daten (Liste von dicts)
        "ppm_axis"      – ppm-Achse
        "spectrum"      – Intensitätswerte
        "figure"        – matplotlib Figure
    """
    peaks = compute_1h_peaks(smiles, seed=seed)

    if verbose:
        print_peak_table(peaks, smiles)

    ppm_axis, spectrum = synthesize_1h_spectrum(peaks, line_width_ppm=line_width)
    fig = plot_1h_nmr(ppm_axis, spectrum, peaks, smiles, show_integrals= show_integrals, show_title= show_title)

    if testrun and plot:
            plt.show()

    if testrun:
        return {"peaks": peaks, "ppm_axis": ppm_axis, "spectrum": spectrum, "figure": fig}
    else:
        return fig


# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    smiles = sys.argv[1] if len(sys.argv) > 1 else "CCO"

    simulate_1h_nmr(smiles, seed=42, plot=True, verbose=False, show_integrals=False, show_title = False)

    # Zum Vergleich mehrere Moleküle:
    for smi in [

    "C/C=C/C",        # trans-2-Buten
    "C/C=C\\C",       # cis-2-Buten
    "C=CC",           # Propen
    "C=CCO",          # Allylalkohol
    "C=CC=O",         # Acrolein
    "CC=O",           # Ethanal
    "O=CC1=CC=CC=C1", # Benzaldehyd
    ]:
        simulate_1h_nmr(smi, plot=True, verbose=True, show_integrals=True, show_title = True, testrun=True)