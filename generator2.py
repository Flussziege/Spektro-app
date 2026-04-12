import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from scipy.ndimage import gaussian_filter1d

import IR_banden
from IR_banden import FUNCTIONAL_GROUPS
from IR_banden import SKELETON_RULES
from IR_banden import AROMATIC_CORE

# ── Aromat-Substitutionsmuster ────────────────────────────────────────────────
# Kerneigenschaft: out-of-plane (oop) C-H Biegeschwingungen der
# benachbarten aromatischen H-Atome → Position hängt von der Anzahl
# zusammenhängender H-Atome im Ring ab.

def get_aromatic_substitution_peaks(mol) -> list[tuple]:
    """
    Gibt oop-Grundschwingungen + Obertöne/Kombinationsbanden (1650–2000 cm⁻¹)
    für jeden Benzolring zurück.
    Format: (wn, intensity, width, label)
    """
    peaks = []

    ring_info = mol.GetRingInfo()
    for ring in ring_info.AtomRings():
        if len(ring) != 6:
            continue
        atoms = [mol.GetAtomWithIdx(i) for i in ring]
        if not all(a.GetIsAromatic() for a in atoms):
            continue

        # ── Ringadjazenz aufbauen ─────────────────────────────────────────
        h_bearing = [i for i in ring
                     if mol.GetAtomWithIdx(i).GetTotalNumHs() > 0]
        adj: dict[int, list[int]] = {i: [] for i in ring}
        for i, idx in enumerate(ring):
            nb_idx = ring[(i + 1) % 6]
            adj[idx].append(nb_idx)
            adj[nb_idx].append(idx)

        # ── Zusammenhängende H-Blöcke ─────────────────────────────────────
        h_set = set(h_bearing)
        visited: set[int] = set()
        blocks = []
        for start in h_bearing:
            if start in visited:
                continue
            block, stack = [], [start]
            while stack:
                node = stack.pop()
                if node in visited:
                    continue
                visited.add(node)
                block.append(node)
                for nb in adj[node]:
                    if nb in h_set and nb not in visited:
                        stack.append(nb)
            blocks.append(len(block))

        # ── Peaks je Substitutionsmuster ──────────────────────────────────
        for n in blocks:

            if n == 5:   # ── monosubstituiert ─────────────────────────────
                peaks += [
                    # Grundschwingungen
                    (3030, 0.45, 14, "ArH str mono"),
                    (1600, 0.50, 16, "Ar C=C I"),
                    (1500, 0.55, 16, "Ar C=C II"),
                    (760,  0.80, 18, "ArH oop 5adj"),
                    (700,  0.75, 16, "ArH oop mono"),
                    # Obertöne & Kombinationen (schwach, aber diagnostisch)
                    # 2×oop(760) ≈ 1520 überlappt C=C, daher die anderen:
                    (1950, 0.08, 22, "Ar overtone I (mono)"),
                    (1870, 0.10, 20, "Ar overtone II (mono)"),
                    (1800, 0.08, 20, "Ar comb. band (mono)"),
                    (1730, 0.06, 18, "Ar comb. band II (mono)"),
                ]

            elif n == 4:  # ── ortho-disubstituiert ─────────────────────────
                peaks += [
                    (3030, 0.40, 14, "ArH str ortho"),
                    (1600, 0.45, 16, "Ar C=C I"),
                    (1500, 0.50, 16, "Ar C=C II"),
                    (750,  0.85, 18, "ArH oop 4adj"),
                    # Obertöne
                    (1950, 0.09, 20, "Ar overtone (ortho)"),
                    (1850, 0.10, 20, "Ar comb. band (ortho)"),
                ]

            elif n == 3:  # ── meta-disubstituiert / 1,2,3-trisubst. ────────
                peaks += [
                    (3030, 0.38, 14, "ArH str meta"),
                    (1600, 0.42, 16, "Ar C=C I"),
                    (1500, 0.48, 16, "Ar C=C II"),
                    (780,  0.70, 18, "ArH oop 3adj"),
                    (690,  0.45, 16, "ArH oop meta"),
                    # Obertöne: 3 Banden charakteristisch für meta
                    (1950, 0.07, 20, "Ar overtone I (meta)"),
                    (1860, 0.09, 18, "Ar overtone II (meta)"),
                    (1800, 0.07, 18, "Ar comb. band (meta)"),
                ]

            elif n == 2:  # ── para-disubstituiert ──────────────────────────
                peaks += [
                    (3030, 0.35, 14, "ArH str para"),
                    (1600, 0.40, 16, "Ar C=C I"),
                    (1500, 0.45, 16, "Ar C=C II"),
                    (830,  0.85, 14, "ArH oop 2adj"),
                    # para hat nur 2 Obertöne → sehr aufgeräumtes Muster
                    (1930, 0.09, 18, "Ar overtone (para)"),
                    (1820, 0.10, 16, "Ar comb. band (para)"),
                ]

            elif n == 1:  # ── 1,3,5-trisubstituiert ────────────────────────
                peaks += [
                    (3030, 0.30, 14, "ArH str 1,3,5"),
                    (1600, 0.35, 16, "Ar C=C I"),
                    (1500, 0.40, 16, "Ar C=C II"),
                    (860,  0.60, 14, "ArH oop 1adj"),
                    # nur 1 isoliertes H → nur eine schwache Oberton-Bande
                    (1900, 0.06, 18, "Ar overtone (1,3,5)"),
                ]

    return peaks

# ══════════════════════════════════════════════════════════════════════════════
#  PEAK-SAMMLUNG
# ══════════════════════════════════════════════════════════════════════════════

def collect_peaks(smiles: str, seed: int = None) -> tuple[np.ndarray, np.ndarray, np.ndarray, list[str]]:
    """
    Sammelt alle Peaks für ein Molekül.
    Gibt (frequencies, intensities, widths, group_labels) zurück.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError(f"Ungültiger SMILES: {smiles}")

    rng = np.random.default_rng(
        seed if seed is not None else sum(ord(c) for c in smiles)
    )

    peaks_raw: list[tuple[float, float, float]] = []
    detected_groups: list[str] = []

    # ── 1. Funktionelle Gruppen ───────────────────────────────────────────────
    # Prioritätsregel: spezifischere Gruppen sperren allgemeinere
    EXCLUSIONS = {
        # wenn Carbonsäure → kein Alkohol, kein Ester
        "carboxylic_acid": ["alcohol_primary", "alcohol_secondary",
                            "alcohol_tertiary", "ester"],
        # wenn Ester → kein allg. Ether
        "ester":           ["ether_aliph"],
        # wenn Amid → kein allg. Amin
        "amide":           ["primary_amine", "secondary_amine"],
        # wenn Anhydrid → kein Ester, keine Säure
        "anhydride":       ["ester", "carboxylic_acid"],
        # terminales Alkin → kein internes
        "terminal_alkyne": ["internal_alkyne"],
        # neu
        "carbamate":       ["amide", "ester", "ether_aliph", "ether_arom"],
        "sulfoxide":       ["thioether"],
        "sulfone":         ["thioether"],
    }
    active_exclusions: set[str] = set()
    
    # Erst Matches prüfen, dann exklusive Gruppen deaktivieren
    matched: dict[str, int] = {}
    for name, gd in FUNCTIONAL_GROUPS.items():
        patt = Chem.MolFromSmarts(gd["smarts"])
        if patt is None:
            continue
        matches = mol.GetSubstructMatches(patt)
        if matches:
            matched[name] = len(matches)
            for excl in EXCLUSIONS.get(name, []):
                active_exclusions.add(excl)

    # cis/trans-Alken: vereinfachte Heuristik
    # (ohne 3D-Info nehmen wir trans als häufiger an)
    if "trans_alkene" in matched and "cis_alkene" in matched:
        active_exclusions.add("cis_alkene")

    for name, count in matched.items():
        if name in active_exclusions:
            continue
        gd = FUNCTIONAL_GROUPS[name]
        detected_groups.append(name)

        scale = np.log1p(count) if gd.get("count") else 1  # max 4-fach skaliert

        for wn, inten, width, label in gd["peaks"]:
            jitter = rng.uniform(-width * 0.15, width * 0.15)
            i_jitter = rng.uniform(0.92, 1.08)
            peaks_raw.append((wn + jitter, inten * scale * i_jitter, width))

    
    # ── Aromatischer Kern ─────────────────────────────
    patt = Chem.MolFromSmarts(AROMATIC_CORE["smarts"])
    if mol.HasSubstructMatch(patt):
        for wn, inten, width, label in AROMATIC_CORE["peaks"]:
            jitter = rng.uniform(-width * 0.1, width * 0.1)
            peaks_raw.append((wn + jitter, inten, width))

    # ── 2. Aromaten-Substitutionsmuster ──────────────────────────────────────
    ar_peaks = get_aromatic_substitution_peaks(mol)
    for wn, inten, width, label in ar_peaks:
        jitter = rng.uniform(-width * 0.1, width * 0.1)
        peaks_raw.append((wn + jitter, inten, width))

    # ── 3. Skelett-Schwingungen ───────────────────────────────────────────────
    for rule in SKELETON_RULES:
        patt = Chem.MolFromSmarts(rule["smarts"])
        if patt is None:
            continue
        matches = mol.GetSubstructMatches(patt)
        if not matches:
            continue
        count = len(matches)
        scale = (min(count / 2, rule.get("max_scale", 2.0))
                 if rule.get("scale_with_count") else 1.0)
        for wn, inten, width, label in rule["peaks"]:
            jitter = rng.uniform(-width * 0.12, width * 0.12)
            peaks_raw.append((wn + jitter, inten * scale, width))

    freqs = np.array([p[0] for p in peaks_raw])
    intens = np.array([p[1] for p in peaks_raw])
    widths = np.array([p[2] for p in peaks_raw])

    return freqs, intens, widths, detected_groups


# ══════════════════════════════════════════════════════════════════════════════
#  SPEKTRUM-SYNTHESE
# ══════════════════════════════════════════════════════════════════════════════

def synthesize_spectrum(
    frequencies: np.ndarray,
    intensities: np.ndarray,
    widths: np.ndarray,
    wn_range: tuple = (500, 4000),
    n_points: int = 4000,
    noise_level: float = 0.006,
    seed: int = 42,
) -> tuple[np.ndarray, np.ndarray]:

    rng = np.random.default_rng(seed)
    wns = np.linspace(wn_range[0], wn_range[1], n_points)
    absorbance = np.zeros(n_points)

    for freq, inten, width in zip(frequencies, intensities, widths):
        diff = wns - freq
        gauss_frac = 0.55
        gauss   = np.exp(-diff**2 / (2 * width**2))
        lorentz = 1.0 / (1.0 + (diff / width)**2)
        peak = inten * (gauss_frac * gauss + (1 - gauss_frac) * lorentz)

        # Breite OH/NH-Banden: Maximum statt Addition
        if 2400 <= freq <= 3700 and width > 40:
            absorbance = np.maximum(absorbance, peak)
        else:
            absorbance += peak * (1 - absorbance)

    # ── Keine globale Normierung mehr ──────────────────────────────────────
    # Stattdessen: weiches Clipping nur gegen physikalisch unmögliche Werte
    # (Absorption > 1 = 0% Transmission, kommt bei sehr starken Carbonyl-
    #  Banden in konzentrierter Lösung vor, ist aber realistisch selten)
    absorbance = np.clip(absorbance, 0.0, 1.0)

    # Rauschen
    white = rng.normal(0, noise_level, n_points)
    noise = gaussian_filter1d(white, sigma=2) * 0.6 \
          + rng.normal(0, noise_level * 0.3, n_points)

    transmittance = np.clip(1.0 - absorbance + noise, 0.02, 1.0)
    return wns, transmittance


# ══════════════════════════════════════════════════════════════════════════════
#  VISUALISIERUNG
# ══════════════════════════════════════════════════════════════════════════════

def plot_ir(wns, transmittance, smiles: str,
            groups: list[str] = None, show_title: bool = True) -> plt.Figure:

    fig, ax = plt.subplots(figsize=(13, 5))
    ax.plot(wns, transmittance * 100, color="#185FA5", linewidth=1.2)
    ax.fill_between(wns, transmittance * 100, 100, alpha=0.05, color="#185FA5")

    ax.set_xlim(4000, 500)
    ax.set_ylim(-2, 105)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(500))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(100))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(20))
    ax.grid(True, which="major", alpha=0.2, linewidth=0.5)
    ax.grid(True, which="minor", alpha=0.08, linewidth=0.3)

    ax.axvspan(500, 1500, alpha=0.03, color="orange")
    ax.text(1000, 3, "Fingerprint", ha="center", fontsize=8,
            color="gray", style="italic")

    ax.set_xlabel("Wellenzahl (cm⁻¹)", fontsize=11)
    ax.set_ylabel("Transmission (%)", fontsize=11)
    if show_title:
        ax.set_title(f"Simulated IR – {smiles}", fontsize=13)
        if groups:
            ax.text(0.99, 0.97, ", ".join(groups), transform=ax.transAxes,
                ha="right", va="top", fontsize=7.5, color="gray")

    else:
        ax.set_title(f"Simulated IR", fontsize=13)

    
    fig.tight_layout()
    return fig


# ══════════════════════════════════════════════════════════════════════════════
#  HAUPT-API
# ══════════════════════════════════════════════════════════════════════════════

def simulate_ir(smiles: str, noise: float = 0.006,
                seed: int = None, plot: bool = True, show_title: bool=True, testrun: bool = False):

    freqs, intens, widths, groups = collect_peaks(smiles, seed=seed)
    wns, trans = synthesize_spectrum(freqs, intens, widths,
                                      noise_level=noise, seed=seed or 42)
    fig = plot_ir(wns, trans, smiles, groups=groups, show_title=show_title)
    
    if testrun and plot:
            plt.show()

    return fig
    




if __name__ == "__main__":
    for smi in [
                "CCCO",               # 1-Propanol
                "CC(=O)O",            # Essigsäure
                "CC(=O)OCC",          # Ethylacetat
                ]:
        simulate_ir(smi, seed=42, plot=True, testrun=True)

