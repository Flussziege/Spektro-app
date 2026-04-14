import numpy as np
from rdkit import Chem
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# ══════════════════════════════════════════════════════════════════════════════
#  INKREMENTE  –  alle Werte in ppm
#  Quellen: Breitmaier/Voelter, Pretsch/Bühlmann, Grant-Paul-Modell
# ══════════════════════════════════════════════════════════════════════════════

# Basis-Shift je nach C-Hybridisierung
BASE_SHIFT = {
    Chem.HybridizationType.SP3:  6.0,   # Methan-artig
    Chem.HybridizationType.SP2: 110.0,  # Alken/Aromat-artig
    Chem.HybridizationType.SP:   65.0,  # Alkin-artig
}

# Inkremente für direkt gebundene Atome (α, also 1 Bindung entfernt)
# Format: SMARTS des Substituenten → ppm-Inkrement
ALPHA_INCREMENTS = [
    # Elektronegative Heteroatome / funktionelle Gruppen
    ("[OX2H]",          40.0),   # OH (Alkohol)
    ("[OX2H0]",         50.0),   # O-R (Ether, Ester-O)
    ("[OX1]",           45.0),   # =O (Carbonyl, direkt am C)
    ("[F]",             70.0),   # Fluor
    ("[Cl]",            31.0),   # Chlor
    ("[Br]",            20.0),   # Brom
    ("[I]",              7.0),   # Iod (schwächerer Effekt)
    ("[NX3H2]",         28.0),   # -NH2
    ("[NX3H1]",         24.0),   # -NHR
    ("[NX3H0]",         20.0),   # -NR2
    ("[N+](=O)[O-]",    63.0),   # -NO2
    ("[SX2]",           11.0),   # Thioether
    ("[SX2H]",          12.0),   # Thiol
    # C-C Bindungen (Grant-Paul α-Inkrement pro C-Nachbar)
    ("[CX4]",            9.1),   # sp3-C Nachbar
    ("[CX3]",            6.0),   # sp2-C Nachbar
    ("[cX3]",            6.0),   # aromatisches C
    ("[CX2]",            4.0),   # sp-C Nachbar
]

# β-Inkremente (2 Bindungen entfernt) – schwächer
BETA_INCREMENTS = [
    ("[OX2H]",           8.0),
    ("[OX2H0]",         10.0),
    ("[OX1]",            3.0),
    ("[F]",              8.0),
    ("[Cl]",             5.5),
    ("[Br]",             3.5),
    ("[I]",              1.5),
    ("[NX3H2]",          6.0),
    ("[NX3H1]",          5.0),
    ("[NX3H0]",          4.0),
    ("[N+](=O)[O-]",     5.0),
    ("[SX2]",            2.5),
    ("[CX4]",            9.4),   # Grant-Paul β-Inkrement
    ("[CX3]",            7.0),
    ("[cX3]",            7.0),
    ("[CX2]",            3.5),
]

# γ-Inkremente (3 Bindungen entfernt) – meist negativ (gauche-Effekt)
GAMMA_INCREMENTS = [
    ("[OX2H]",          -1.5),
    ("[OX2H0]",         -2.0),
    ("[F]",             -2.0),
    ("[Cl]",            -2.5),
    ("[Br]",            -3.0),
    ("[NX3H2]",         -2.5),
    ("[N+](=O)[O-]",    -2.0),
    ("[CX4]",           -2.5),   # Grant-Paul γ-Inkrement
    ("[CX3]",           -1.5),
    ("[cX3]",           -1.5),
]

# Spezielle Korrekturterme für bestimmte C-Typen
# Wird nach α/β/γ addiert
SPECIAL_CORRECTIONS = [
    # Carbonyl-Kohlenstoffe
    ("[CX3](=O)[OH]",     178.0, True),   # COOH  → absoluter Override
    ("[CX3](=O)[OX2][#6]",165.0, True),   # Ester-C=O
    ("[CX3H0](=O)[#6]",   197.0, True),   # Keton
    ("[CX3H1](=O)",       200.0, True),   # Aldehyd-C
    ("[CX2]#[NX1]",       118.0, True),   # Nitril-C
    # Aromatische C mit Substituenten
    ("[cX3][OX2]",        155.0, True),   # ArO- (phenolisches C)
    ("[cX3][NX3]",        148.0, True),   # ArN-
    ("[cX3][F]",          162.0, True),   # ArF
    ("[cX3][Cl]",         134.0, True),   # ArCl
    ("[cX3][Br]",         122.0, True),   # ArBr
    ("[cX3][N+](=O)[O-]", 148.0, True),   # Ar-NO2
]


# ══════════════════════════════════════════════════════════════════════════════
#  KERN-FUNKTION: Shift-Berechnung per Atom
# ══════════════════════════════════════════════════════════════════════════════

def _get_neighbors_at_distance(mol, atom_idx: int, distance: int) -> list[int]:
    """Gibt alle Atom-Indices zurück, die genau `distance` Bindungen entfernt sind."""
    if distance == 0:
        return [atom_idx]
    
    visited = {atom_idx}
    frontier = {atom_idx}
    
    for _ in range(distance):
        next_frontier = set()
        for idx in frontier:
            for nb in mol.GetAtomWithIdx(idx).GetNeighbors():
                if nb.GetIdx() not in visited:
                    next_frontier.add(nb.GetIdx())
        visited |= next_frontier
        frontier = next_frontier
    
    return list(frontier)


def _apply_increments(mol, neighbor_indices: list[int],
                      increment_table: list[tuple]) -> float:
    """Summiert alle passenden Inkremente für eine Liste von Nachbar-Atomen."""
    total = 0.0
    for nb_idx in neighbor_indices:
        atom = mol.GetAtomWithIdx(nb_idx)
        # Jedes Inkrement-SMARTS gegen dieses eine Atom testen
        for smarts, value in increment_table:
            patt = Chem.MolFromSmarts(smarts)
            if patt is None:
                continue
            # Substruktur-Match eingeschränkt auf dieses eine Atom
            for match in mol.GetSubstructMatches(patt):
                if match[0] == nb_idx:
                    total += value
                    break  # pro Nachbar + SMARTS nur einmal zählen
    return total


def calculate_shift(atom_idx: int, mol) -> float:
    """
    Berechnet den 13C-Shift für ein C-Atom durch:
      1. Basis-Shift (Hybridisierung)
      2. α-Inkremente (direkte Nachbarn, ohne das Atom selbst)
      3. β-Inkremente (Nachbarn 2 Bindungen entfernt)
      4. γ-Inkremente (Nachbarn 3 Bindungen entfernt)
      5. Spezielle Override-Korrekturen (z.B. Carbonyle)
    """
    atom = mol.GetAtomWithIdx(atom_idx)
    hyb  = atom.GetHybridization()
    
    # 1. Basis
    shift = BASE_SHIFT.get(hyb, 30.0)
    
    # 2–4. Nachbar-Inkremente
    alpha_nb = _get_neighbors_at_distance(mol, atom_idx, 1)
    beta_nb  = _get_neighbors_at_distance(mol, atom_idx, 2)
    gamma_nb = _get_neighbors_at_distance(mol, atom_idx, 3)
    
    shift += _apply_increments(mol, alpha_nb,  ALPHA_INCREMENTS)
    shift += _apply_increments(mol, beta_nb,   BETA_INCREMENTS)
    shift += _apply_increments(mol, gamma_nb,  GAMMA_INCREMENTS)
    
    # 5. Spezielle Overrides (absoluter Wert, wenn Muster passt)
    for smarts, override_val, is_absolute in SPECIAL_CORRECTIONS:
        patt = Chem.MolFromSmarts(smarts)
        if patt is None:
            continue
        for match in mol.GetSubstructMatches(patt):
            if match[0] == atom_idx:
                if is_absolute:
                    return override_val   # direkt zurück, kein weiteres Summieren
                else:
                    shift += override_val
                break
    
    return shift


# ══════════════════════════════════════════════════════════════════════════════
#  ÄQUIVALENZKLASSEN + PEAK-BERECHNUNG
# ══════════════════════════════════════════════════════════════════════════════

def rule_based_peaks(smiles: str, seed: int = None) -> tuple[np.ndarray, np.ndarray]:
    """
    Gibt (frequencies, intensities) zurück.
    Äquivalente C-Atome (gleicher canonical rank) → ein Peak,
    Intensität = Anzahl äquivalenter Atome.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError(f"Ungültiger SMILES: {smiles}")
    
    rng = np.random.default_rng(
        seed if seed is not None else sum(ord(c) for c in smiles)
    )
    
    # Äquivalente Atome via Morgan-Ranks (breakTies=False!)
    ranks = list(Chem.CanonicalRankAtoms(mol, breakTies=False))
    
    rank_to_atoms: dict[int, list[int]] = {}
    for atom in mol.GetAtoms():
        if atom.GetAtomicNum() == 6:
            r = ranks[atom.GetIdx()]
            rank_to_atoms.setdefault(r, []).append(atom.GetIdx())
    
    frequencies, intensities = [], []
    
    for atom_list in rank_to_atoms.values():
        rep = atom_list[0]                          # repräsentatives Atom
        base = calculate_shift(rep, mol)
        shift = round(base + rng.normal(0, 0.5), 1) # minimales Rauschen
        frequencies.append(shift)
        intensities.append(len(atom_list))
    
    return np.array(frequencies), np.array(intensities, dtype=float)


# ══════════════════════════════════════════════════════════════════════════════
#  SPEKTRUM-SYNTHESE & PLOT  (unverändert, leicht aufgeräumt)
# ══════════════════════════════════════════════════════════════════════════════

def synthesize_spectrum(frequencies, intensities,
                        n_points=3500, wn_range=(0, 220),
                        width=0.5, seed=42):
    wns = np.linspace(wn_range[1], wn_range[0], n_points)
    spectrum = np.zeros(n_points)
    for f, i in zip(frequencies, intensities):
        spectrum += i * np.exp(-(wns - f)**2 / (2 * width**2))
    return wns, spectrum


def plot_nmr(wns, spectrum, smiles, frequencies=None,
             intensities=None, groups=None, show_title=True):
    fig, ax = plt.subplots(figsize=(13, 5))
    ax.plot(wns, spectrum, color="#185FA5", linewidth=1.2)
    ax.fill_between(wns, spectrum, 0, alpha=0.07, color="#185FA5")
    

    
    ax.set_xlim(220, 0)
    ax.set_ylim(bottom=0)
    ax.xaxis.set_major_locator(ticker.MultipleLocator(20))
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(5))
    ax.grid(True, which="major", alpha=0.2, linewidth=0.5)
    ax.grid(True, which="minor", alpha=0.08, linewidth=0.3)
    ax.set_xlabel("Chemical Shift (ppm)", fontsize=11)
    ax.set_ylabel("Intensity (rel.)", fontsize=11)
    if show_title:
        ax.set_title(f"Simulated ¹³C NMR – {smiles}", fontsize=13)
    else:
        ax.set_title(f"Simulated ¹³C NMR", fontsize=13)
    if groups:
        ax.text(0.99, 0.97, "Groups: " + ", ".join(groups),
                transform=ax.transAxes, ha="right", va="top",
                fontsize=8, color="gray")
    fig.tight_layout()
    return fig


def simulate_13c_nmr(smiles: str, seed: int = None,
                     plot: bool = True, width: float = 0.035,
                     show_title: bool = True, testrun: bool = False, 
                     easymode: bool = False):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError(f"Ungültiger SMILES: {smiles}")
    
    freqs, intens = rule_based_peaks(smiles, seed=seed)

    rng = np.random.default_rng(
        seed if seed is not None else sum(ord(c) for c in smiles)
    )

    if easymode:
        plot_intens = intens.astype(float)
    else:
        plot_intens = np.array([
            max(0.2, 1.0 + rng.normal(0, 0.08)) for _ in intens
        ], dtype=float)

    groups = []
    for smarts, _ in ALPHA_INCREMENTS:
        patt = Chem.MolFromSmarts(smarts)
        if patt and mol.HasSubstructMatch(patt):
            groups.append(smarts)
    
    wns, spectrum = synthesize_spectrum(
        freqs, plot_intens,
        wn_range=(0, 220), width=width
    )
    
    fig = plot_nmr(
        wns, spectrum, smiles,
        frequencies=freqs, intensities=plot_intens, show_title=show_title
    )

    if testrun:
        return {
            "frequencies": freqs,
            "intensities": plot_intens,
            "wns": wns,
            "spectrum": spectrum,
            "figure": fig,
            "groups": groups,
        }

    if plot:
        plt.show()

    return fig

# ── Tests ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    tests = {
        "Ethanol":        "CCO",
        "Ethan-1,1-diol": "OCC(O)O",   # 2× OH am selben C → stärkerer Shift
        "test1": "CCOC",
        "test2": "CCOCC",
        #"Dimethylether":  "COC",        # 2 äquivalente CH3 → 1 Peak, I=2
        #"Essigsäure":     "CC(=O)O",
        #"Benzol":         "c1ccccc1",   # 6 äquivalente C → 1 Peak, I=6
        #"Chloroform":     "ClC(Cl)Cl",
    }
    for name, smi in tests.items():
        print(f"\n{'═'*50}")
        print(f"  {name}")
        simulate_13c_nmr(smi, seed=42, plot=True, testrun=True, easymode=False)