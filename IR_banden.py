# ══════════════════════════════════════════════════════════════════════════════
#  PEAK-TABELLEN
#  Format: (Wellenzahl, Intensität, Breite_cm-1, Label)
#  Intensität 1.0 = stärkste Bande des Spektrums
# ══════════════════════════════════════════════════════════════════════════════


# ── Funktionelle Gruppen ─────────────────────────────────────────────────────

FUNCTIONAL_GROUPS: dict[str, dict] = {

    # ── C-H sp3 ──────────────────────────────────────────────────────────────
    "METHANE": {
        "smarts": "[CX4H4]",
        "count": False,
        "peaks": [
            # Fundamentals
            (3010, 0.35, 12, "CH4 asym str"),
            (1305, 0.25, 14, "CH4 bend"),
            (2970, 0.12, 10, "Fermi shoulder"),
            (3050, 0.10, 10, "Fermi shoulder"),

            # Obertöne / Kombinationen (realistisch schwach!)
            (2600, 0.08, 18, "2*CH4 bend"),
            (2800, 0.06, 16, "combination band"),
        ]
    },
    "CH3": {
        "smarts": "[CX4H3]",
        "count": True,   # Intensität skaliert mit Anzahl der Matches
        "peaks": [
            (2962, 0.40, 12, "CH3 asym str"),   # war 0.55  
            (2872, 0.36, 10, "CH3 sym str"),    # war 0.50
            (1460, 0.22, 14, "CH3 asym def"),   # war 0.35
            (1375, 0.28, 10, "CH3 sym def"),    # war 0.40
            (1165, 0.12, 18, "CH3 rock"),       # war 0.20
            # Obertöne und schwache Schwingungen
            (1481, 0.02, 16, "2*CH3 asym str overtone"),
            (1436, 0.02, 14, "2*CH3 sym str overtone"),
            (730,  0.05, 20, "CH3 combination band"),
        ]
    },
    "CH2": {
        "smarts": "[CX4H2]",
        "count": True,
        "peaks": [
            (2926, 0.45, 12, "CH2 asym str"),   # war 0.60
            (2855, 0.40, 10, "CH2 sym str"),    # war 0.55
            (1465, 0.25, 14, "CH2 scissor"),    # war 0.35
            (1350, 0.10, 16, "CH2 wag"),        # war 0.15
            (1250, 0.10, 18, "CH2 twist"),      # war 0.15
            (720,  0.18, 14, "CH2 rock"),       # war 0.25
            # Obertöne und schwache Schwingungen
            (1463, 0.02, 16, "2*CH2 asym str overtone"),
            (1428, 0.02, 14, "2*CH2 sym str overtone"),
            (360,  0.03, 20, "CH2 combination band"),
        ]
    },
    "CH_sp3": {
        "smarts": "[CX4H1]",
        "count": True,
        "peaks": [
            (2890, 0.40, 14, "CH str"),
            (1340, 0.20, 16, "CH bend"),
            # Obertöne und schwache Schwingungen
            (1445, 0.02, 16, "2*CH str overtone"),
            (670,  0.03, 18, "CH combination band"),
        ]
    },

    # ── C-H sp2 / Alken ──────────────────────────────────────────────────────
    "vinyl_CH2": {
        "smarts": "[CX3H2]=[CX3]",
        "count": True,
        "peaks": [
            (3090, 0.45, 12, "=CH2 asym str"),
            (3000, 0.40, 10, "=CH2 sym str"),
            (1640, 0.50, 20, "C=C str"),
            (990,  0.55, 14, "=CH2 oop"),
            (910,  0.65, 14, "=CH2 wag"),   # sehr charakteristisch
            # Obertöne
            (1820, 0.02, 16, "2*=CH2 oop overtone"),
        ]
    },
    "trans_alkene": {
        "smarts": "[CX3H]=[CX3H]",   # wird weiter unten auf cis/trans geprüft
        "count": False,
        "peaks": [
            (3020, 0.40, 12, "=CH str"),
            (1670, 0.45, 20, "C=C str trans"),
            (970,  0.70, 14, "=CH oop trans"),  # sehr stark und charakteristisch
            # Obertöne
            (1940, 0.02, 16, "2*=CH oop trans overtone"),
        ]
    },
    "cis_alkene": {
        "smarts": "[CX3H]=[CX3H]",
        "count": False,
        "peaks": [
            (3010, 0.40, 12, "=CH str"),
            (1650, 0.45, 20, "C=C str cis"),
            (730,  0.55, 18, "=CH oop cis"),
            # Obertöne
            (1460, 0.02, 16, "2*=CH oop cis overtone"),
        ]
    },
    "trisubst_alkene": {
        "smarts": "[CX3H1]=[CX3H0]",
        "count": False,
        "peaks": [
            (3020, 0.35, 12, "=CH str"),
            (1660, 0.40, 20, "C=C str"),
            (820,  0.45, 16, "=CH oop"),
            # Obertöne
            (1640, 0.02, 16, "2*=CH oop overtone"),
        ]
    },

    # ── Alkin ────────────────────────────────────────────────────────────────
    "terminal_alkyne": {
        "smarts": "[CX2H]#[CX2]",
        "count": False,
        "peaks": [
            (3300, 0.60, 10, "≡C-H str"),
            (2120, 0.55, 16, "C≡C str terminal"),
            (680,  0.40, 14, "≡C-H bend"),
            # Obertöne
            (1360, 0.02, 16, "2*≡C-H bend overtone"),
        ]
    },
    "internal_alkyne": {
        "smarts": "[CX2H0]#[CX2H0]",
        "count": False,
        "peaks": [
            (2190, 0.30, 16, "C≡C str internal"),  # schwächer (kein Dipolmoment)
        ]
    },

    # ── Carbonyle ────────────────────────────────────────────────────────────
    "carboxylic_acid": {
        "smarts": "[CX3](=O)[OX2H1]",
        "count": False,
        "peaks": [
            # ── C=O Stretch (scharf, stark) ──────────────────────────────
            (1710, 0.95, 22,  "C=O str (COOH)"),
            (1320, 0.45, 25,  "C-O str"),
            (1250, 0.40, 25,  "C-O str II"),
            (940,  0.35, 30,  "OH oop (COOH)"),

            # Obertöne
            (855,  0.03, 20, "2*C=O str overtone"),

            # ── OH-Stretch: breiter, unförmiger "Säuresack" ───────────────
            # Wird NICHT mit Maximum-Methode behandelt sondern addiert
            # → natürliche Unregelmäßigkeit durch Überlagerung
            (3020, 0.55, 280, "OH broad I"),       # Hauptbuckel, asymm.
            (2950, 0.50, 200, "OH broad II"),      # leicht versetzt
            (2850, 0.42, 180, "OH broad III"),     # Schulter tief
            (2670, 0.28, 140, "OH broad IV"),      # untere Flanke
            (2560, 0.18, 110, "OH broad V"),       # Ausläufer
            # Fermi-Resonanz-Schultern (charakteristische Dellen/Höcker)
            (2990, 0.12,  45, "Fermi shoulder I"),
            (2900, 0.12,  40, "Fermi shoulder II"),
            (2730, 0.12,  35, "Fermi shoulder III"),
        ]
    },
    "ester": {
        "smarts": "[CX3](=O)[OX2H0][#6]",
        "count": False,
        "peaks": [
            (1735, 1.00, 18, "C=O str (ester)"),
            (1240, 0.65, 30, "C-O-C asym str"),
            (1050, 0.45, 28, "C-O-C sym str"),
            # Obertöne
            (868, 0.03, 18, "2*C=O str overtone"),
        ]
    },
    "ketone": {
        "smarts": "[#6X3](=O)([#6])[#6]",
        "count": False,
        "peaks": [
            (1715, 0.95, 20, "C=O str (ketone)"),
            (1220, 0.30, 22, "C-C-C str"),
            # Obertöne
            (858, 0.03, 18, "2*C=O str overtone"),
        ]
    },
    "aldehyde": {
        "smarts": "[CX3H1](=O)",
        "count": False,
        "peaks": [
            (2820, 0.35, 14, "CHO str (Fermi I)"),
            (2720, 0.30, 14, "CHO str (Fermi II)"),
            (1725, 0.95, 20, "C=O str (aldehyde)"),
            (1390, 0.25, 18, "CH bend (CHO)"),
            # Obertöne
            (863, 0.03, 18, "2*C=O str overtone"),
        ]
    },
    "formaldehyde": {
        "smarts": "[CX3H2](=O)",
        "count": False,
        "peaks": [
            (3540, 0.08, 10, "very weak overtone / combination"),
            (3510, 0.06, 10, "very weak overtone / combination"),
            (3335, 0.20, 16, "weak overtone / combination"),
            (3190, 0.05, 18, "weak overtone / combination"),
            (3060, 0.06, 20, "C-H stretch region (weak)"),
            (2985, 0.32, 24, "C-H stretch / combination band"),
            (2905, 0.28, 26, "C-H stretch / combination band"),
            (2845, 0.72, 22, "CHO str (Fermi I)"),
            (2775, 0.88, 18, "CHO str (Fermi II)"),
            (2715, 0.24, 22, "CHO stretch shoulder"),
            (1735, 0.98, 24, "C=O str (aldehyde)"),
            (1605, 0.12, 18, "weak deformation / combination"),
            (1560, 0.14, 20, "weak deformation / combination"),
            (1495, 0.52, 12, "CH bend / deformation"),
            (1460, 0.10, 12, "CH deformation"),
            (1425, 0.06, 10, "CH deformation"),
            (1385, 0.08, 12, "CH bend (CHO)"),
            (1350, 0.05, 10, "CH wag / deformation"),
            (1295, 0.10, 14, "skeletal / CH wag"),
            (1240, 0.28, 22, "CH wag / deformation"),
            (1175, 0.14, 16, "CH wag"),
            (1135, 0.22, 18, "CH rock / deformation"),
            (1095, 0.48, 18, "CH rock"),
            (1045, 0.48, 20, "CH in-plane bend"),
            (995, 0.35, 18, "CH wag / skeletal mode"),
            (960, 0.40, 18, "CH out-of-plane bend"),
            (930, 0.42, 16, "rocking / skeletal mode"),
            (885, 0.65, 18, "strong deformation / out-of-plane mode"),
            (820, 0.12, 18, "skeletal deformation"),
            (760, 0.12, 18, "CHO out-of-plane bend"),
            (705, 0.12, 16, "skeletal deformation"),
            (625, 0.22, 18, "low-frequency deformation"),
            (590, 0.12, 16, "low-frequency deformation"),
            # Obertöne
            (868, 0.03, 18, "2*C=O str overtone")
        ]
    },
    "primary_amide": {
        "smarts": "[CX3](=O)[NX3H2]",
        "count": False,
        "peaks": [
            (3350, 0.50, 50, "NH2 asym str"),
            (3180, 0.45, 50, "NH2 sym str"),
            (1660, 0.95, 25, "C=O str (amide I)"),
            (1550, 0.65, 25, "NH2 bend (amide II)"),
            # Obertöne
            (830, 0.03, 20, "2*C=O str overtone"),
        ]
    },
    "secondary_amide": {
        "smarts": "[CX3](=O)[NX3H1]",
        "count": False,
        "peaks": [
            (3300, 0.50, 50, "NH str"),
            (1660, 0.95, 25, "C=O str (amide I)"),
            (1550, 0.65, 25, "NH bend (amide II)"),
        ]
    },
    "tertiary_amide": {
        "smarts": "[CX3](=O)[NX3H0]",
        "count": False,
        "peaks": [
            (1660, 0.95, 25, "C=O str (amide I)"),
            (1550, 0.65, 25, "amide II"),
            # Obertöne
            (830, 0.03, 20, "2*C=O str overtone"),
        ]
    },
    "anhydride": {
        "smarts": "[CX3](=O)[OX2][CX3](=O)",
        "count": False,
        "peaks": [
            (1850, 0.80, 18, "C=O asym str (anhydride)"),
            (1760, 0.90, 18, "C=O sym str (anhydride)"),
            (1040, 0.55, 25, "C-O-C str"),
        ]
    },

    # ── O-H / N-H ────────────────────────────────────────────────────────────
    "alcohol_primary": {
        "smarts": "[CX4H2][OX2H]",
        "count": False,
        "peaks": [
            (3340, 0.55, 80,  "OH str (prim alc, H-bond)"),
            (1060, 0.50, 25,  "C-O str prim"),
            (1030, 0.35, 20,  "C-O str prim II"),
            (660,  0.25, 30,  "OH oop"),
        ]
    },
    "alcohol_secondary": {
        "smarts": "[CX4H1][OX2H]",
        "count": False,
        "peaks": [
            (3350, 0.50, 75,  "OH str (sec alc)"),
            (1110, 0.50, 25,  "C-O str sec"),
            (660,  0.20, 30,  "OH oop"),
        ]
    },
    "alcohol_tertiary": {
        "smarts": "[CX4H0][OX2H]",
        "count": False,
        "peaks": [
            (3360, 0.45, 70,  "OH str (tert alc)"),
            (1150, 0.50, 25,  "C-O str tert"),
        ]
    },
    "phenol": {
        "smarts": "[OX2H][cX3]",
        "count": False,
        "peaks": [
            (3300, 0.55, 90,  "OH str (phenol)"),
            (1230, 0.55, 25,  "C-O str phenol"),
            (750,  0.35, 20,  "OH oop phenol"),
        ]
    },

    # ── Ether ────────────────────────────────────────────────────────────────
    "ether_aliph": {
        "smarts": "[CX4][OX2H0][CX4]",
        "count": False,
        "peaks": [
            (1120, 0.60, 30, "C-O-C asym str"),
            (1000, 0.35, 25, "C-O-C sym str"),
        ]
    },
    "ether_arom": {
        "smarts": "[cX3][OX2H0][#6]",
        "count": False,
        "peaks": [
            (1250, 0.55, 28, "Ar-O-C asym str"),
            (1040, 0.40, 25, "Ar-O-C sym str"),
        ]
    },
    "epoxide": {
        "smarts": "[CX4]1O[CX4]1",
        "count": False,
        "peaks": [
            (1260, 0.55, 18, "epoxide ring str"),
            (920,  0.45, 16, "epoxide ring bend"),
            (830,  0.40, 14, "epoxide ring bend II"),
            # Obertöne
            (1840, 0.02, 16, "2*epoxide ring bend overtone"),
        ]
    },

    # ── Stickstoff ───────────────────────────────────────────────────────────
    "primary_amine": {
        "smarts": "[NX3H2][#6]",
        "count": False,
        "peaks": [
            (3380, 0.50, 55, "NH2 asym str"),
            (3300, 0.45, 50, "NH2 sym str"),
            (1615, 0.45, 30, "NH2 scissor"),
            (800,  0.30, 25, "NH2 wag"),
            # Obertöne
            (1600, 0.02, 16, "2*NH2 scissor overtone"),
        ]
    },
    "secondary_amine": {
        "smarts": "[NX3H1]([#6])[#6]",
        "count": False,
        "peaks": [
            (3320, 0.35, 45, "N-H str (sec)"),
            (1510, 0.30, 25, "N-H bend"),
            # Obertöne
            (3020, 0.02, 16, "2*N-H bend overtone"),
        ]
    },
    "nitrile": {
        "smarts": "[CX2]#[NX1]",
        "count": False,
        "peaks": [
            (2240, 0.65, 16, "C≡N str"),
        ]
    },
    "nitro": {
        "smarts": "[N+](=O)[O-]",
        "count": False,
        "peaks": [
            (1540, 0.90, 22, "NO2 asym str"),
            (1370, 0.80, 20, "NO2 sym str"),
            (860,  0.30, 18, "NO2 oop"),
        ]
    },
    "imine_NH": {
        "smarts": "[CX3]=[NX2H]",
        "count": False,
        "peaks": [
            (1650, 0.55, 20, "C=N str"),
            (3320, 0.25, 40, "N-H str"),
            # Obertöne
            (3300, 0.02, 16, "2*C=N str overtone"),
        ]
    },
    "imine_substituted": {
        "smarts": "[CX3]=[NX2H0]",
        "count": False,
        "peaks": [
            (1650, 0.55, 20, "C=N str"),
            # Obertöne
            (3300, 0.02, 16, "2*C=N str overtone"),
        ]
    },

    # ── Halogene ─────────────────────────────────────────────────────────────
    "C_F": {
        "smarts": "[CX4][F]",
        "count": True,
        "peaks": [
            (1100, 0.75, 30, "C-F str"),
            (1050, 0.55, 25, "C-F str II"),
        ]
    },
    "C_Cl": {
        "smarts": "[CX4][Cl]",
        "count": True,
        "peaks": [
            (760,  0.60, 20, "C-Cl str"),
            (700,  0.40, 18, "C-Cl str II"),
            # Obertöne
            (1520, 0.02, 16, "2*C-Cl str overtone"),
        ]
    },
    # ── Schwefel ─────────────────────────────────────────────────────────────
    "thiol": {
        "smarts": "[SX2H]",
        "count": False,
        "peaks": [
            (2570, 0.20, 14, "S-H str"),   # sehr schwach!
            (700,  0.25, 18, "C-S str"),
        ]
    },
    "thioether": {
        "smarts": "[SX2H0]([#6])[#6]",
        "count": False,
        "peaks": [
            (700,  0.30, 18, "C-S str"),
            (650,  0.20, 16, "C-S str II"),
        ]
    },

    # ── Phosphor ─────────────────────────────────────────────────────────────
    "phosphate": {
        "smarts": "[PX4](=O)([OX2])[OX2]",
        "count": False,
        "peaks": [
            (1260, 0.70, 25, "P=O str"),
            (1050, 0.60, 28, "P-O-C str"),
        ]
    },
}

FUNCTIONAL_GROUPS.update({

    "METHANE": {
        "smarts": "[CX4H4]",
        "count": False,
        "peaks": [
            (3016, 0.36, 12, "CH4 asym str"),
            (3004, 0.30, 12, "CH4 asym str II"),
            (1306, 0.28, 14, "CH4 bend"),
            (1535, 0.08, 18, "combination band"),
            (2975, 0.14, 10, "Fermi shoulder I"),
            (3050, 0.12, 10, "Fermi shoulder II"),
            (2815, 0.08, 16, "combination band"),
            (2600, 0.08, 18, "2*CH4 bend"),
            (1760, 0.05, 18, "overtone / combination"),
        ]
    },

    "CH3": {
        "smarts": "[CX4H3]",
        "count": True,
        "peaks": [
            (2972, 0.22, 10, "CH3 asym str shoulder"),
            (2962, 0.40, 12, "CH3 asym str"),
            (2940, 0.12, 10, "CH3 stretch shoulder"),
            (2885, 0.14, 10, "CH3 stretch shoulder II"),
            (2872, 0.36, 10, "CH3 sym str"),
            (1458, 0.22, 14, "CH3 asym def"),
            (1438, 0.10, 12, "CH3 deformation"),
            (1415, 0.08, 12, "CH3 deformation II"),
            (1375, 0.28, 10, "CH3 sym def"),
            (1360, 0.10, 10, "CH3 sym def shoulder"),
            (1265, 0.06, 16, "CH3 twist"),
            (1195, 0.08, 16, "CH3 wag"),
            (1165, 0.12, 18, "CH3 rock"),
            (1120, 0.06, 16, "CH3 rock II"),
            (1045, 0.05, 16, "CH3 rocking / skeletal"),
            (980,  0.06, 14, "CH3 rocking"),
        ]
    },

    "CH2": {
        "smarts": "[CX4H2]",
        "count": True,
        "peaks": [
            (2932, 0.20, 10, "CH2 asym str shoulder"),
            (2926, 0.45, 12, "CH2 asym str"),
            (2916, 0.16, 10, "CH2 asym str II"),
            (2865, 0.14, 10, "CH2 sym str shoulder"),
            (2855, 0.40, 10, "CH2 sym str"),
            (1472, 0.12, 12, "CH2 deformation"),
            (1465, 0.25, 14, "CH2 scissor"),
            (1452, 0.10, 12, "CH2 scissor shoulder"),
            (1418, 0.06, 12, "CH2 deformation II"),
            (1350, 0.10, 16, "CH2 wag"),
            (1305, 0.08, 16, "CH2 wag II"),
            (1250, 0.10, 18, "CH2 twist"),
            (1230, 0.06, 16, "CH2 twist shoulder"),
            (1170, 0.06, 16, "CH2 deformation"),
            (1125, 0.05, 16, "CH2 rocking / skeletal"),
            (970,  0.05, 14, "CH2 rocking"),
            (720,  0.18, 14, "CH2 rock"),
        ]
    },

    "CH_sp3": {
        "smarts": "[CX4H1]",
        "count": True,
        "peaks": [
            (2895, 0.18, 12, "CH str shoulder"),
            (2890, 0.40, 14, "CH str"),
            (2868, 0.10, 12, "CH str II"),
            (1460, 0.10, 14, "CH deformation"),
            (1380, 0.08, 14, "CH bend shoulder"),
            (1340, 0.20, 16, "CH bend"),
            (1260, 0.08, 16, "CH wag"),
            (1180, 0.06, 16, "CH rocking"),
            (1120, 0.05, 16, "skeletal / CH mode"),
        ]
    },

    "vinyl_CH2": {
        "smarts": "[CX3H2]=[CX3]",
        "count": True,
        "peaks": [
            (3100, 0.18, 10, "=CH2 str shoulder"),
            (3090, 0.45, 12, "=CH2 asym str"),
            (3075, 0.16, 10, "=CH2 asym str II"),
            (3010, 0.12, 10, "=CH2 sym str shoulder"),
            (3000, 0.40, 10, "=CH2 sym str"),
            (1640, 0.50, 20, "C=C str"),
            (1615, 0.08, 16, "C=C str shoulder"),
            (1415, 0.12, 14, "=CH2 deformation"),
            (1295, 0.08, 14, "=CH2 twist"),
            (1245, 0.06, 14, "=CH2 wag"),
            (990,  0.55, 14, "=CH2 oop"),
            (960,  0.18, 14, "=CH2 oop shoulder"),
            (910,  0.65, 14, "=CH2 wag"),
        ]
    },

    "trans_alkene": {
        "smarts": "[CX3H]=[CX3H]",
        "count": False,
        "peaks": [
            (3030, 0.18, 10, "=CH str shoulder"),
            (3020, 0.40, 12, "=CH str"),
            (1670, 0.45, 20, "C=C str trans"),
            (1635, 0.08, 16, "C=C shoulder"),
            (1445, 0.08, 14, "=CH bend"),
            (1310, 0.08, 14, "=CH in-plane"),
            (1240, 0.06, 14, "=CH in-plane II"),
            (970,  0.70, 14, "=CH oop trans"),
        ]
    },

    "cis_alkene": {
        "smarts": "[CX3H]=[CX3H]",
        "count": False,
        "peaks": [
            (3020, 0.16, 10, "=CH str shoulder"),
            (3010, 0.40, 12, "=CH str"),
            (1650, 0.45, 20, "C=C str cis"),
            (1625, 0.08, 16, "C=C shoulder"),
            (1440, 0.08, 14, "=CH bend"),
            (1300, 0.08, 14, "=CH in-plane"),
            (1225, 0.06, 14, "=CH in-plane II"),
            (730,  0.55, 18, "=CH oop cis"),
        ]
    },

    "trisubst_alkene": {
        "smarts": "[CX3H1]=[CX3H0]",
        "count": False,
        "peaks": [
            (3030, 0.12, 10, "=CH str shoulder"),
            (3020, 0.35, 12, "=CH str"),
            (1660, 0.40, 20, "C=C str"),
            (1630, 0.08, 16, "C=C shoulder"),
            (1450, 0.08, 14, "=CH bend"),
            (1290, 0.08, 14, "=CH in-plane"),
            (1240, 0.06, 14, "=CH wag"),
            (820,  0.45, 16, "=CH oop"),
        ]
    },

    "terminal_alkyne": {
        "smarts": "[CX2H]#[CX2]",
        "count": False,
        "peaks": [
            (3310, 0.18, 10, "≡C-H str shoulder"),
            (3300, 0.60, 10, "≡C-H str"),
            (3260, 0.06, 10, "≡C-H overtone / shoulder"),
            (2120, 0.55, 16, "C≡C str terminal"),
            (2085, 0.08, 14, "C≡C shoulder"),
            (1280, 0.06, 14, "≡C-H bend / combination"),
            (680,  0.40, 14, "≡C-H bend"),
        ]
    },

    "internal_alkyne": {
        "smarts": "[CX2H0]#[CX2H0]",
        "count": False,
        "peaks": [
            (2190, 0.30, 16, "C≡C str internal"),
            (2145, 0.06, 14, "C≡C shoulder"),
            (1260, 0.05, 14, "skeletal / combination"),
            (660,  0.06, 14, "skeletal bend"),
        ]
    },

    "carboxylic_acid": {
        "smarts": "[CX3](=O)[OX2H1]",
        "count": False,
        "peaks": [
            (1710, 0.95, 22,  "C=O str (COOH)"),
            (1685, 0.12, 18,  "C=O shoulder"),
            (1440, 0.18, 20,  "OH in-plane bend"),
            (1320, 0.45, 25,  "C-O str"),
            (1290, 0.18, 22,  "C-O str shoulder"),
            (1250, 0.40, 25,  "C-O str II"),
            (1215, 0.20, 22,  "C-OH bend / C-O str"),
            (1175, 0.10, 20,  "C-OH deformation"),
            (1130, 0.08, 18,  "COOH deformation"),
            (1040, 0.06, 18,  "skeletal / OH mode"),
            (980,  0.10, 18,  "OH wag"),
            (940,  0.35, 30,  "OH oop (COOH)"),
            (890,  0.10, 20,  "COOH deformation II"),

            (3020, 0.55, 280, "OH broad I"),
            (2950, 0.50, 200, "OH broad II"),
            (2850, 0.42, 180, "OH broad III"),
            (2670, 0.28, 140, "OH broad IV"),
            (2560, 0.18, 110, "OH broad V"),

            (2990, 0.12,  45, "Fermi shoulder I"),
            (2900, 0.12,  40, "Fermi shoulder II"),
            (2730, 0.12,  35, "Fermi shoulder III"),
        ]
    },

    "ester": {
        "smarts": "[CX3](=O)[OX2H0][#6]",
        "count": False,
        "peaks": [
            (1742, 0.22, 16, "C=O shoulder"),
            (1735, 1.00, 18, "C=O str (ester)"),
            (1718, 0.10, 16, "C=O low shoulder"),
            (1275, 0.24, 20, "C-O-C asym str shoulder"),
            (1240, 0.65, 30, "C-O-C asym str"),
            (1210, 0.18, 18, "C-O stretch"),
            (1175, 0.22, 18, "C-O stretch II"),
            (1125, 0.16, 18, "C-O-C deformation"),
            (1090, 0.14, 18, "C-O stretch III"),
            (1050, 0.45, 28, "C-O-C sym str"),
            (1020, 0.12, 18, "C-O-C sym str II"),
            (980,  0.06, 16, "skeletal / ester mode"),
        ]
    },

    "ketone": {
        "smarts": "[#6X3](=O)([#6])[#6]",
        "count": False,
        "peaks": [
            (1720, 0.18, 16, "C=O shoulder"),
            (1715, 0.95, 20, "C=O str (ketone)"),
            (1700, 0.10, 16, "C=O low shoulder"),
            (1460, 0.12, 16, "alpha-CH deformation"),
            (1420, 0.08, 16, "skeletal deformation"),
            (1365, 0.08, 16, "CH deformation"),
            (1220, 0.30, 22, "C-C-C str"),
            (1170, 0.08, 18, "skeletal mode"),
            (1110, 0.06, 18, "skeletal mode II"),
        ]
    },

    "aldehyde": {
        "smarts": "[CX3H1](=O)",
        "count": False,
        "peaks": [
            (2840, 0.14, 12, "CHO str shoulder"),
            (2820, 0.35, 14, "CHO str (Fermi I)"),
            (2760, 0.10, 12, "CHO combination"),
            (2720, 0.30, 14, "CHO str (Fermi II)"),
            (1735, 0.14, 16, "C=O shoulder"),
            (1725, 0.95, 20, "C=O str (aldehyde)"),
            (1710, 0.10, 16, "C=O low shoulder"),
            (1460, 0.08, 14, "CHO / alpha-CH deformation"),
            (1390, 0.25, 18, "CH bend (CHO)"),
            (1260, 0.08, 16, "CHO wag / deformation"),
            (1170, 0.08, 16, "skeletal / CH mode"),
            (1110, 0.06, 16, "skeletal mode"),
            (980,  0.06, 14, "CHO wag"),
            (930,  0.06, 14, "CHO oop"),
        ]
    },

    "formaldehyde": {
        "smarts": "[CX3H2](=O)",
        "count": False,
        "peaks": [
            (3540, 0.08, 10, "very weak overtone / combination"),
            (3510, 0.06, 10, "very weak overtone / combination"),
            (3335, 0.20, 16, "weak overtone / combination"),
            (3190, 0.05, 18, "weak overtone / combination"),
            (3060, 0.06, 20, "C-H stretch region (weak)"),
            (2985, 0.32, 24, "C-H stretch / combination band"),
            (2905, 0.28, 26, "C-H stretch / combination band"),
            (2845, 0.72, 22, "CHO str (Fermi I)"),
            (2775, 0.88, 18, "CHO str (Fermi II)"),
            (2715, 0.24, 22, "CHO stretch shoulder"),
            (1735, 0.98, 24, "C=O str (aldehyde)"),
            (1605, 0.12, 18, "weak deformation / combination"),
            (1560, 0.14, 20, "weak deformation / combination"),
            (1495, 0.52, 12, "CH bend / deformation"),
            (1460, 0.10, 12, "CH deformation"),
            (1425, 0.06, 10, "CH deformation"),
            (1385, 0.08, 12, "CH bend (CHO)"),
            (1350, 0.05, 10, "CH wag / deformation"),
            (1295, 0.10, 14, "skeletal / CH wag"),
            (1240, 0.28, 22, "CH wag / deformation"),
            (1175, 0.14, 16, "CH wag"),
            (1135, 0.22, 18, "CH rock / deformation"),
            (1095, 0.48, 18, "CH rock"),
            (1045, 0.48, 20, "CH in-plane bend"),
            (995,  0.35, 18, "CH wag / skeletal mode"),
            (960,  0.40, 18, "CH out-of-plane bend"),
            (930,  0.42, 16, "rocking / skeletal mode"),
            (885,  0.65, 18, "strong deformation / out-of-plane mode"),
            (820,  0.12, 18, "skeletal deformation"),
            (760,  0.12, 18, "CHO out-of-plane bend"),
            (705,  0.12, 16, "skeletal deformation"),
            (625,  0.22, 18, "low-frequency deformation"),
            (590,  0.12, 16, "low-frequency deformation")
        ]
    },

    "amide": {
        "smarts": "[CX3](=O)[NX3]",
        "count": False,
        "peaks": [
            (3350, 0.50, 50, "NH2 asym str"),
            (3180, 0.45, 50, "NH2 sym str"),
            (1660, 0.95, 25, "C=O str (amide I)"),
            (1550, 0.65, 25, "NH2 bend (amide II)"),
        ]
    },
    "anhydride": {
        "smarts": "[CX3](=O)[OX2][CX3](=O)",
        "count": False,
        "peaks": [
            (1850, 0.80, 18, "C=O asym str (anhydride)"),
            (1815, 0.18, 16, "C=O asym shoulder"),
            (1760, 0.90, 18, "C=O sym str (anhydride)"),
            (1735, 0.14, 16, "C=O sym shoulder"),
            (1300, 0.24, 20, "C-O str"),
            (1230, 0.20, 18, "C-O-C asym str"),
            (1100, 0.18, 18, "C-O-C deformation"),
            (1040, 0.55, 25, "C-O-C str"),
            (930,  0.12, 18, "skeletal mode"),
            (900,  0.10, 18, "skeletal mode II"),
        ]
    },

    "alcohol_primary": {
        "smarts": "[CX4H2][OX2H]",
        "count": False,
        "peaks": [
            (3470, 0.16, 70,  "OH str free shoulder"),
            (3340, 0.55, 80,  "OH str (prim alc, H-bond)"),
            (1420, 0.12, 18,  "OH in-plane bend"),
            (1270, 0.08, 18,  "C-OH deformation"),
            (1125, 0.12, 20,  "C-O str prim shoulder"),
            (1060, 0.50, 25,  "C-O str prim"),
            (1030, 0.35, 20,  "C-O str prim II"),
            (980,  0.08, 18,  "OH wag"),
            (660,  0.25, 30,  "OH oop"),
            (620,  0.08, 20,  "OH oop shoulder"),
        ]
    },

    "alcohol_secondary": {
        "smarts": "[CX4H1][OX2H]",
        "count": False,
        "peaks": [
            (3480, 0.14, 65,  "OH str free shoulder"),
            (3350, 0.50, 75,  "OH str (sec alc)"),
            (1415, 0.10, 18,  "OH in-plane bend"),
            (1260, 0.08, 18,  "C-OH deformation"),
            (1140, 0.14, 20,  "C-O str sec shoulder"),
            (1110, 0.50, 25,  "C-O str sec"),
            (1080, 0.18, 18,  "C-O str sec II"),
            (980,  0.06, 18,  "OH wag"),
            (660,  0.20, 30,  "OH oop"),
        ]
    },

    "alcohol_tertiary": {
        "smarts": "[CX4H0][OX2H]",
        "count": False,
        "peaks": [
            (3490, 0.12, 60,  "OH str free shoulder"),
            (3360, 0.45, 70,  "OH str (tert alc)"),
            (1410, 0.08, 18,  "OH in-plane bend"),
            (1190, 0.14, 18,  "C-O str tert shoulder"),
            (1150, 0.50, 25,  "C-O str tert"),
            (1120, 0.16, 18,  "C-O str tert II"),
            (980,  0.05, 18,  "OH wag"),
        ]
    },

    "phenol": {
        "smarts": "[OX2H][cX3]",
        "count": False,
        "peaks": [
            (3560, 0.10, 45,  "OH str free shoulder"),
            (3300, 0.55, 90,  "OH str (phenol)"),
            (1410, 0.10, 18,  "OH in-plane bend"),
            (1270, 0.16, 18,  "Ar-O str shoulder"),
            (1230, 0.55, 25,  "C-O str phenol"),
            (1180, 0.14, 18,  "Ar-O str II"),
            (1150, 0.10, 18,  "phenolic deformation"),
            (980,  0.08, 18,  "OH wag"),
            (750,  0.35, 20,  "OH oop phenol"),
            (690,  0.10, 16,  "Ar-O deformation"),
        ]
    },

    "ether_aliph": {
        "smarts": "[CX4][OX2H0][CX4]",
        "count": False,
        "peaks": [
            (1145, 0.16, 18, "C-O-C asym str shoulder"),
            (1120, 0.60, 30, "C-O-C asym str"),
            (1090, 0.20, 18, "C-O-C asym str II"),
            (1060, 0.18, 18, "C-O stretch"),
            (1030, 0.16, 18, "C-O stretch II"),
            (1000, 0.35, 25, "C-O-C sym str"),
            (975,  0.10, 16, "C-O-C sym str II"),
            (930,  0.08, 16, "skeletal / ether mode"),
            (840,  0.06, 16, "C-O-C deformation"),
        ]
    },

    "ether_arom": {
        "smarts": "[cX3][OX2H0][#6]",
        "count": False,
        "peaks": [
            (1270, 0.16, 18, "Ar-O-C asym shoulder"),
            (1250, 0.55, 28, "Ar-O-C asym str"),
            (1210, 0.14, 18, "Ar-O stretch"),
            (1175, 0.18, 18, "Ar-O-C deformation"),
            (1040, 0.40, 25, "Ar-O-C sym str"),
            (1015, 0.14, 18, "Ar-O-C sym str II"),
            (845,  0.10, 16, "Ar-O deformation"),
            (760,  0.08, 16, "Ar-O deformation II"),
        ]
    },

    "epoxide": {
        "smarts": "[CX4]1O[CX4]1",
        "count": False,
        "peaks": [
            (1260, 0.55, 18, "epoxide ring str"),
            (1230, 0.16, 16, "epoxide ring str II"),
            (1160, 0.10, 16, "C-O-C ring mode"),
            (950,  0.12, 16, "ring deformation"),
            (920,  0.45, 16, "epoxide ring bend"),
            (870,  0.10, 14, "ring deformation II"),
            (830,  0.40, 14, "epoxide ring bend II"),
        ]
    },

    "primary_amine": {
        "smarts": "[NX3H2][#6]",
        "count": False,
        "peaks": [
            (3450, 0.18, 40, "NH2 asym shoulder"),
            (3380, 0.50, 55, "NH2 asym str"),
            (3300, 0.45, 50, "NH2 sym str"),
            (1615, 0.45, 30, "NH2 scissor"),
            (1585, 0.12, 20, "NH2 scissor shoulder"),
            (1300, 0.10, 18, "C-N / NH wag"),
            (1250, 0.08, 18, "C-N str"),
            (1170, 0.08, 18, "C-N / skeletal"),
            (930,  0.08, 18, "NH wag"),
            (800,  0.30, 25, "NH2 wag"),
            (760,  0.10, 18, "NH2 wag II"),
        ]
    },

    "secondary_amine": {
        "smarts": "[NX3H1]([#6])[#6]",
        "count": False,
        "peaks": [
            (3320, 0.35, 45, "N-H str (sec)"),
            (1510, 0.30, 25, "N-H bend"),
            (1450, 0.10, 18, "CH/NH deformation"),
            (1290, 0.10, 18, "C-N str"),
            (1180, 0.08, 18, "C-N / skeletal"),
            (750,  0.10, 18, "N-H wag"),
        ]
    },

    "nitrile": {
        "smarts": "[CX2]#[NX1]",
        "count": False,
        "peaks": [
            (2250, 0.14, 12, "C≡N str shoulder"),
            (2240, 0.65, 16, "C≡N str"),
            (2220, 0.08, 12, "C≡N low shoulder"),
            (1450, 0.06, 16, "skeletal deformation"),
            (1220, 0.06, 16, "C-C≡N mode"),
            (970,  0.05, 14, "skeletal / CN mode"),
        ]
    },

    "nitro": {
        "smarts": "[N+](=O)[O-]",
        "count": False,
        "peaks": [
            (1560, 0.16, 18, "NO2 asym shoulder"),
            (1540, 0.90, 22, "NO2 asym str"),
            (1515, 0.14, 18, "NO2 asym str II"),
            (1390, 0.14, 18, "NO2 sym shoulder"),
            (1370, 0.80, 20, "NO2 sym str"),
            (1350, 0.14, 18, "NO2 sym str II"),
            (1290, 0.10, 18, "C-NO2 str"),
            (860,  0.30, 18, "NO2 oop"),
            (760,  0.12, 16, "NO2 deformation"),
            (720,  0.08, 16, "NO2 deformation II"),
        ]
    },

    "C_F": {
        "smarts": "[CX4][F]",
        "count": True,
        "peaks": [
            (1220, 0.10, 20, "C-F str shoulder"),
            (1160, 0.16, 20, "C-F str"),
            (1120, 0.60, 30, "C-F str strong"),
            (1090, 0.18, 22, "C-F str II"),
            (1050, 0.45, 25, "C-F str III"),
            (1010, 0.12, 20, "C-F str IV"),
        ]
    },

    "C_Cl": {
        "smarts": "[CX4][Cl]",
        "count": True,
        "peaks": [
            (790,  0.14, 16, "C-Cl str shoulder"),
            (760,  0.60, 20, "C-Cl str"),
            (730,  0.16, 18, "C-Cl str II"),
            (700,  0.40, 18, "C-Cl str III"),
            (650,  0.10, 16, "C-Cl deformation"),
        ]
    },

    "C_Br": {
        "smarts": "[CX4][Br]",
        "count": True,
        "peaks": [
            (690,  0.12, 16, "C-Br str shoulder"),
            (650,  0.55, 20, "C-Br str"),
            (610,  0.16, 18, "C-Br str II"),
            # Obertöne
            (1300, 0.02, 16, "2*C-Br str overtone"),
        ]
    },

    "thiol": {
        "smarts": "[SX2H]",
        "count": False,
        "peaks": [
            (2570, 0.20, 14, "S-H str"),
            (930,  0.05, 16, "S-H bend / combination"),
            (700,  0.25, 18, "C-S str"),
            (660,  0.08, 16, "C-S str II"),
        ]
    },

    "thioether": {
        "smarts": "[SX2H0]([#6])[#6]",
        "count": False,
        "peaks": [
            (750,  0.10, 16, "C-S-C deformation"),
            (700,  0.30, 18, "C-S str"),
            (650,  0.20, 16, "C-S str II"),
            (620,  0.08, 16, "C-S deformation"),
        ]
    },

    "phosphate": {
        "smarts": "[PX4](=O)([OX2])[OX2]",
        "count": False,
        "peaks": [
            (1260, 0.70, 25, "P=O str"),
            (1215, 0.18, 20, "P=O shoulder"),
            (1160, 0.18, 20, "P-O stretch"),
            (1090, 0.20, 20, "P-O-C str shoulder"),
            (1050, 0.60, 28, "P-O-C str"),
            (1020, 0.16, 20, "P-O-C str II"),
            (970,  0.12, 18, "P-O deformation"),
            (890,  0.08, 18, "P-O bending"),
        ]
    },
})

FUNCTIONAL_GROUPS.update({
    "pyrrol": {
        "smarts": "[nH]1cccc1",
        "count": False,
        "peaks": [
            (3480, 0.18, 40, "N-H str"),
            (3120, 0.16, 12, "aromatic C-H str"),
            (3090, 0.18, 12, "aromatic C-H str II"),
            (1575, 0.22, 18, "ring C=C/C-N str"),
            (1490, 0.20, 18, "ring stretch"),
            (1415, 0.16, 16, "C-N / ring mode"),
            (1290, 0.18, 18, "C-N str"),
            (1180, 0.14, 18, "ring breathing / CH bend"),
            (1040, 0.12, 16, "C-H in-plane"),
            (930,  0.12, 16, "ring deformation"),
            (760,  0.18, 16, "C-H oop"),
        ]
    },

    "furan": {
        "smarts": "o1cccc1",
        "count": False,
        "peaks": [
            (3140, 0.14, 12, "aromatic C-H str"),
            (3110, 0.16, 12, "aromatic C-H str II"),
            (1590, 0.18, 18, "ring C=C str"),
            (1505, 0.22, 18, "ring stretch"),
            (1460, 0.14, 16, "ring stretch II"),
            (1275, 0.26, 18, "C-O-C ring str"),
            (1160, 0.20, 18, "C-O-C / ring mode"),
            (1070, 0.18, 18, "ring breathing"),
            (1015, 0.14, 16, "C-H in-plane"),
            (930,  0.12, 16, "ring deformation"),
            (745,  0.16, 16, "C-H oop"),
        ]
    },

    "thiophen": {
        "smarts": "s1cccc1",
        "count": False,
        "peaks": [
            (3110, 0.14, 12, "aromatic C-H str"),
            (3085, 0.16, 12, "aromatic C-H str II"),
            (1510, 0.20, 18, "ring C=C str"),
            (1450, 0.18, 18, "ring stretch"),
            (1410, 0.12, 16, "ring stretch II"),
            (1250, 0.12, 18, "ring mode"),
            (1085, 0.16, 18, "ring breathing"),
            (1040, 0.12, 16, "C-H in-plane"),
            (845,  0.16, 16, "C-H oop"),
            (705,  0.22, 16, "C-S / ring deformation"),
        ]
    },
})

# ── Kohlenstoffgerüst-Schwingungen (immer vorhanden, kontext-abhängig) ────────

SKELETON_RULES: list[dict] = [
    # C-C Streckschwingungen
    {
        "smarts": "[CX4][CX4]",
        "peaks": [(1000, 0.12, 20, "C-C str"), (900, 0.10, 18, "C-C str II")],
        "scale_with_count": True,
        "max_scale": 3.0,
    },
    # Isopropyl-Dublett (sehr charakteristisch)
    {
        "smarts": "[CH3][CX4H][CH3]",
        "peaks": [
            (1385, 0.35, 10, "iPr sym def"),
            (1370, 0.35, 10, "iPr asym def"),
        ],
        "scale_with_count": False,
    },
    # tert-Butyl
    {
        "smarts": "[CH3][CX4]([CH3])[CH3]",
        "peaks": [
            (1395, 0.25, 10, "tBu def"),
            (1365, 0.40, 10, "tBu sym def"),
        ],
        "scale_with_count": False,
    },
    # C-N Streckschwingungen aliphatisch
    {
        "smarts": "[CX4][NX3]",
        "peaks": [(1090, 0.25, 22, "C-N str aliph")],
        "scale_with_count": True,
        "max_scale": 2.0,
    },
    # C-N aromatisch
    {
        "smarts": "[cX3][NX3]",
        "peaks": [(1340, 0.45, 22, "C-N str arom"), (1260, 0.35, 20, "C-N str arom II")],
        "scale_with_count": False,
    },
]

FUNCTIONAL_GROUPS.update({
    "acid_chloride": {
        "smarts": "[CX3](=O)[Cl]",
        "count": False,
        "peaks": [
            (1810, 1.00, 18, "C=O str (acid chloride)"),
            (1788, 0.18, 16, "C=O shoulder"),
            (1435, 0.08, 16, "skeletal deformation"),
            (1260, 0.16, 18, "C-C(=O)-Cl mode"),
            (980,  0.08, 16, "skeletal mode"),
            (790,  0.45, 16, "C-Cl str (acyl chloride)"),
        ]
    },

    "sulfoxide": {
        "smarts": "[SX3](=O)([#6])[#6]",
        "count": False,
        "peaks": [
            (1060, 0.24, 18, "S=O str shoulder"),
            (1035, 0.92, 22, "S=O str (sulfoxide)"),
            (990,  0.14, 18, "S=O / C-S mode"),
            (950,  0.10, 16, "skeletal deformation"),
            (760,  0.18, 16, "C-S str"),
            (700,  0.10, 16, "C-S deformation"),
        ]
    },

    "sulfone": {
        "smarts": "[SX4](=O)(=O)([#6])[#6]",
        "count": False,
        "peaks": [
            (1330, 0.18, 18, "SO2 asym shoulder"),
            (1315, 0.95, 20, "SO2 asym str"),
            (1290, 0.14, 18, "SO2 asym str II"),
            (1165, 0.22, 18, "SO2 sym shoulder"),
            (1145, 0.86, 20, "SO2 sym str"),
            (1125, 0.16, 18, "SO2 sym str II"),
            (980,  0.10, 18, "S-C / SO2 mode"),
            (760,  0.16, 16, "C-S str"),
        ]
    },

    "carbamate": {
        "smarts": "[NX3][CX3](=O)[OX2H0][#6]",
        "count": False,
        "peaks": [
            (3360, 0.35, 45, "NH str (carbamate)"),
            (3250, 0.18, 40, "NH str shoulder"),
            (1725, 0.14, 16, "C=O shoulder"),
            (1705, 0.86, 20, "C=O str (carbamate)"),
            (1540, 0.45, 22, "NH bend / amide II-like"),
            (1265, 0.40, 20, "C-O-C / C-N str"),
            (1225, 0.22, 18, "C-N / C-O str"),
            (1160, 0.28, 18, "C-O str"),
            (1060, 0.10, 18, "skeletal mode"),
            (770,  0.10, 18, "NH wag"),
        ]
    },
})

# ── Kohlenstoffgerüst-Schwingungen (immer vorhanden, kontext-abhängig) ────────

AROMATIC_CORE = {
    "smarts": "c1ccccc1",
    "peaks": [
        (3100, 0.10, 10, "ArH str shoulder"),
        (3080, 0.35, 10, "ArH str"),
        (3060, 0.40, 10, "ArH str"),
        (3030, 0.45, 12, "ArH str"),

        (2000, 0.06, 18, "overtone"),
        (1950, 0.10, 20, "overtone"),
        (1905, 0.08, 18, "combination"),
        (1870, 0.12, 18, "overtone"),
        (1835, 0.08, 18, "combination"),
        (1800, 0.10, 18, "combination"),
        (1730, 0.06, 16, "combination"),

        (1600, 0.65, 14, "Ar C=C"),
        (1580, 0.18, 12, "Ar C=C shoulder"),
        (1500, 0.55, 14, "Ar C=C"),
        (1450, 0.35, 12, "Ar C=C"),

        (1310, 0.08, 16, "C-H in-plane"),
        (1275, 0.10, 16, "C-H in-plane"),
        (1175, 0.25, 18, "C-H in-plane"),
        (1150, 0.10, 16, "C-H in-plane II"),
        (1100, 0.20, 18, "C-H in-plane"),
        (1070, 0.08, 16, "ring mode"),
        (1030, 0.30, 16, "C-H in-plane"),
        (1000, 0.40, 16, "ring breathing"),

        (900,  0.08, 16, "ArH oop"),
        (860,  0.08, 16, "ArH oop"),
        (820,  0.08, 16, "ArH oop"),
        (760,  0.10, 14, "ArH oop"),
        (690,  0.75, 14, "ArH oop"),
    ]
}
