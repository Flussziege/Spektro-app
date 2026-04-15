from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple
import math
import random

from rdkit import Chem
from rdkit.Chem import Descriptors, rdMolDescriptors
import plotly.graph_objects as go


# ============================================================
# Data classes
# ============================================================

@dataclass
class Peak:
    mz: float
    intensity: float
    label: str
    kind: str = "fragment"
    fragment_smiles: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MoleculeFeatures:
    formula: str
    exact_mass: float
    carbon_count: int
    hetero_counts: Dict[str, int]
    aromatic_ring_count: int

    has_alcohol: bool = False
    has_phenol: bool = False
    has_carboxylic_acid: bool = False
    has_ester: bool = False
    has_ketone: bool = False
    has_aldehyde: bool = False
    has_amide: bool = False
    has_anhydride: bool = False
    has_ether_aliphatic: bool = False
    has_ether_aromatic: bool = False
    has_epoxide: bool = False
    has_primary_amine: bool = False
    has_secondary_amine: bool = False
    has_tertiary_amine: bool = False
    has_nitrile: bool = False
    has_nitro: bool = False
    has_imine: bool = False
    has_thiol: bool = False
    has_thioether: bool = False
    has_terminal_alkyne: bool = False
    has_internal_alkyne: bool = False
    has_alkene: bool = False
    has_aromatic: bool = False
    has_halogen_cl: bool = False
    has_halogen_br: bool = False
    has_halogen_f: bool = False
    has_halogen_i: bool = False

    carbonyl_like: bool = False


# ============================================================
# SMARTS patterns
# ============================================================

SMARTS: Dict[str, str] = {
    "alcohol": "[CX4][OX2H]",
    "phenol": "c[OX2H]",
    "carboxylic_acid": "[CX3](=O)[OX2H]",
    "ester": "[CX3](=O)[OX2][#6]",
    "ketone": "[#6][CX3](=O)[#6]",
    "aldehyde": "[CX3H1](=O)[#6]",
    "amide": "[NX3][CX3](=O)[#6]",
    "anhydride": "[CX3](=O)O[CX3](=O)",
    "ether_aliphatic": "[#6][OX2][#6]",
    "ether_aromatic": "c[OX2][#6]",
    "epoxide": "[OX2r3]1[#6r3][#6r3]1",
    "primary_amine": "[NX3;H2][#6]",
    "secondary_amine": "[NX3;H1]([#6])[#6]",
    "tertiary_amine": "[NX3]([#6])([#6])[#6]",
    "nitrile": "[CX2]#N",
    "nitro": "[NX3+](=O)[O-]",
    "imine": "[CX3]=[NX2]",
    "thiol": "[#6][SX2H]",
    "thioether": "[#6][SX2][#6]",
    "terminal_alkyne": "[CX2]#[CX2H]",
    "internal_alkyne": "[CX2]#[CX2]",
    "alkene": "[CX3]=[CX3]",
}


def _compile_smarts() -> Dict[str, Chem.Mol]:
    compiled: Dict[str, Chem.Mol] = {}
    for key, smarts in SMARTS.items():
        patt = Chem.MolFromSmarts(smarts)
        if patt is not None:
            compiled[key] = patt
    return compiled


COMPILED_SMARTS = _compile_smarts()


# ============================================================
# Utility
# ============================================================

def _safe_mol_from_smiles(smiles: str) -> Chem.Mol:
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError(f"Ungültiges SMILES: {smiles}")
    return mol


def _count_atoms(mol: Chem.Mol, atomic_num: int) -> int:
    return sum(1 for atom in mol.GetAtoms() if atom.GetAtomicNum() == atomic_num)


def _count_aromatic_rings(mol: Chem.Mol) -> int:
    ring_info = mol.GetRingInfo()
    count = 0
    for ring in ring_info.AtomRings():
        if all(mol.GetAtomWithIdx(idx).GetIsAromatic() for idx in ring):
            count += 1
    return count


def _has_substructure(mol: Chem.Mol, key: str) -> bool:
    patt = COMPILED_SMARTS.get(key)
    return bool(patt and mol.HasSubstructMatch(patt))


def _match_count(mol: Chem.Mol, key: str) -> int:
    patt = COMPILED_SMARTS.get(key)
    if patt is None:
        return 0
    return len(mol.GetSubstructMatches(patt))


def _round_mz(mz: float, digits: int = 4) -> float:
    return round(float(mz), digits)


def _jitter(value: float, rng: random.Random, low: float = 0.92, high: float = 1.08) -> float:
    return value * rng.uniform(low, high)


def _is_aromatic_fragment(mol: Chem.Mol) -> bool:
    return any(atom.GetIsAromatic() for atom in mol.GetAtoms())


def _contains_hetero(mol: Chem.Mol) -> bool:
    return any(atom.GetAtomicNum() not in (1, 6) for atom in mol.GetAtoms())


def _count_carbon_neighbors(atom: Chem.Atom) -> int:
    return sum(1 for nbr in atom.GetNeighbors() if nbr.GetAtomicNum() == 6)


# ============================================================
# Feature extraction
# ============================================================

def extract_molecule_features(smiles: str) -> MoleculeFeatures:
    mol = _safe_mol_from_smiles(smiles)

    formula = rdMolDescriptors.CalcMolFormula(mol)
    exact_mass = rdMolDescriptors.CalcExactMolWt(mol)
    aromatic_ring_count = _count_aromatic_rings(mol)

    hetero_counts = {
        "N": _count_atoms(mol, 7),
        "O": _count_atoms(mol, 8),
        "F": _count_atoms(mol, 9),
        "P": _count_atoms(mol, 15),
        "S": _count_atoms(mol, 16),
        "Cl": _count_atoms(mol, 17),
        "Br": _count_atoms(mol, 35),
        "I": _count_atoms(mol, 53),
    }

    features = MoleculeFeatures(
        formula=formula,
        exact_mass=exact_mass,
        carbon_count=_count_atoms(mol, 6),
        hetero_counts=hetero_counts,
        aromatic_ring_count=aromatic_ring_count,
        has_alcohol=_has_substructure(mol, "alcohol"),
        has_phenol=_has_substructure(mol, "phenol"),
        has_carboxylic_acid=_has_substructure(mol, "carboxylic_acid"),
        has_ester=_has_substructure(mol, "ester"),
        has_ketone=_has_substructure(mol, "ketone"),
        has_aldehyde=_has_substructure(mol, "aldehyde"),
        has_amide=_has_substructure(mol, "amide"),
        has_anhydride=_has_substructure(mol, "anhydride"),
        has_ether_aliphatic=_has_substructure(mol, "ether_aliphatic"),
        has_ether_aromatic=_has_substructure(mol, "ether_aromatic"),
        has_epoxide=_has_substructure(mol, "epoxide"),
        has_primary_amine=_has_substructure(mol, "primary_amine"),
        has_secondary_amine=_has_substructure(mol, "secondary_amine"),
        has_tertiary_amine=_has_substructure(mol, "tertiary_amine"),
        has_nitrile=_has_substructure(mol, "nitrile"),
        has_nitro=_has_substructure(mol, "nitro"),
        has_imine=_has_substructure(mol, "imine"),
        has_thiol=_has_substructure(mol, "thiol"),
        has_thioether=_has_substructure(mol, "thioether"),
        has_terminal_alkyne=_has_substructure(mol, "terminal_alkyne"),
        has_internal_alkyne=_has_substructure(mol, "internal_alkyne"),
        has_alkene=_has_substructure(mol, "alkene"),
        has_aromatic=aromatic_ring_count > 0,
        has_halogen_cl=hetero_counts["Cl"] > 0,
        has_halogen_br=hetero_counts["Br"] > 0,
        has_halogen_f=hetero_counts["F"] > 0,
        has_halogen_i=hetero_counts["I"] > 0,
    )

    features.carbonyl_like = any(
        [
            features.has_carboxylic_acid,
            features.has_ester,
            features.has_ketone,
            features.has_aldehyde,
            features.has_amide,
            features.has_anhydride,
        ]
    )

    return features


# ============================================================
# Fragment helpers
# ============================================================

def _find_cleavable_bonds(mol: Chem.Mol) -> List[Chem.Bond]:
    """
    Heuristik:
    - nur Einfachbindungen
    - bevorzugt C-C, C-O, C-N, C-S
    - keine Ringbindungen
    - keine Aromatenbindungen
    """
    cleavable: List[Chem.Bond] = []

    allowed_pairs = {
        (6, 6),
        (6, 7),
        (7, 6),
        (6, 8),
        (8, 6),
        (6, 16),
        (16, 6),
        (7, 8),
        (8, 7),
    }

    for bond in mol.GetBonds():
        if bond.GetBondType() != Chem.rdchem.BondType.SINGLE:
            continue
        if bond.IsInRing():
            continue

        a1 = bond.GetBeginAtom()
        a2 = bond.GetEndAtom()

        if a1.GetIsAromatic() or a2.GetIsAromatic():
            # benzyliche Bindungen sollen über Stabilitätsbonus
            # auf Fragmentebene sichtbar werden, aber nicht den Ring selbst spalten
            pass

        pair = (a1.GetAtomicNum(), a2.GetAtomicNum())
        if pair in allowed_pairs:
            cleavable.append(bond)

    return cleavable


def _split_molecule_on_bond(mol: Chem.Mol, bond_idx: int) -> List[Chem.Mol]:
    fragmented = Chem.FragmentOnBonds(mol, [bond_idx], addDummies=False)
    frags = Chem.GetMolFrags(fragmented, asMols=True, sanitizeFrags=True)
    return list(frags)


def _fragment_mass(mol: Chem.Mol) -> float:
    return rdMolDescriptors.CalcExactMolWt(mol)


def _fragment_smiles(mol: Chem.Mol) -> str:
    return Chem.MolToSmiles(mol)


def _estimate_fragment_stability(fragment: Chem.Mol) -> float:
    """
    Didaktischer Stabilitäts-Score.
    """
    score = 1.0

    if _is_aromatic_fragment(fragment):
        score += 0.6

    if _contains_hetero(fragment):
        score += 0.25

    # einfache Bonuslogik für stärker substituierte C-Zentren
    carbon_sub_scores = []
    for atom in fragment.GetAtoms():
        if atom.GetAtomicNum() == 6 and not atom.GetIsAromatic():
            carbon_sub_scores.append(_count_carbon_neighbors(atom))

    if carbon_sub_scores:
        best = max(carbon_sub_scores)
        if best >= 3:
            score += 0.35
        elif best == 2:
            score += 0.20
        elif best == 1:
            score += 0.10

    # sehr kleine Fragmente leicht abwerten
    heavy_atoms = fragment.GetNumHeavyAtoms()
    if heavy_atoms <= 2:
        score *= 0.75
    elif heavy_atoms <= 4:
        score *= 0.90

    return score


def _bond_is_alpha_to_hetero(bond: Chem.Bond) -> bool:
    a1 = bond.GetBeginAtom()
    a2 = bond.GetEndAtom()

    for atom, other in ((a1, a2), (a2, a1)):
        if atom.GetAtomicNum() == 6:
            if any(nbr.GetAtomicNum() in (7, 8, 16) and nbr.GetIdx() != other.GetIdx() for nbr in atom.GetNeighbors()):
                return True

    return False


# ============================================================
# Peak generation
# ============================================================

def _generate_molecular_ion_peak(features: MoleculeFeatures, rng: random.Random) -> Peak:
    intensity = 20.0

    if features.has_aromatic:
        intensity += 10
    if features.carbonyl_like:
        intensity += 6
    if features.has_halogen_cl or features.has_halogen_br:
        intensity += 5

    # aliphatische, flexible Moleküle -> M+ tendenziell schwächer
    if not features.has_aromatic and not features.carbonyl_like and features.carbon_count >= 5:
        intensity -= 8

    intensity = max(8.0, min(40.0, _jitter(intensity, rng, 0.9, 1.1)))

    return Peak(
        mz=_round_mz(features.exact_mass),
        intensity=intensity,
        label="M⁺",
        kind="molecular_ion",
    )


def _generate_neutral_loss_peaks(features: MoleculeFeatures, rng: random.Random) -> List[Peak]:
    peaks: List[Peak] = []
    m = features.exact_mass

    def add_loss(loss_mass: float, label: str, base_intensity: float) -> None:
        mz = m - loss_mass
        if mz <= 5:
            return
        peaks.append(
            Peak(
                mz=_round_mz(mz),
                intensity=_jitter(base_intensity, rng),
                label=label,
                kind="neutral_loss",
            )
        )

    if features.has_alcohol or features.has_phenol or features.has_carboxylic_acid:
        add_loss(18.0106, "M−18 (H₂O)", 48.0)

    if features.carbonyl_like:
        add_loss(27.9949, "M−28 (CO)", 36.0)

    if features.has_carboxylic_acid or features.has_ester or features.has_anhydride:
        add_loss(43.9898, "M−44 (CO₂)", 52.0)

    # CH3-Verlust häufiger bei aliphatischen/alkoxyhaltigen Molekülen
    if features.carbon_count >= 2:
        base = 24.0
        if features.has_ether_aliphatic or features.has_ester:
            base += 10.0
        add_loss(15.0235, "M−15 (CH₃)", base)

    # vereinfachte McLafferty-Heuristik
    if features.carbonyl_like and features.carbon_count >= 4:
        add_loss(28.0313, "McLafferty (−C₂H₄)", 62.0)

    return peaks


def _generate_cleavage_peaks(mol: Chem.Mol, rng: random.Random) -> List[Peak]:
    peaks: List[Peak] = []

    for bond in _find_cleavable_bonds(mol):
        frags = _split_molecule_on_bond(mol, bond.GetIdx())
        if len(frags) != 2:
            continue

        alpha_to_hetero = _bond_is_alpha_to_hetero(bond)

        for frag in frags:
            heavy_atoms = frag.GetNumHeavyAtoms()
            if heavy_atoms < 2:
                continue

            mz = _fragment_mass(frag)
            if mz < 10:
                continue

            stability = _estimate_fragment_stability(frag)
            intensity = 18.0 * stability

            label = "bond cleavage"
            kind = "cleavage"

            if alpha_to_hetero:
                intensity *= 1.6
                label = "α-cleavage next to heteroatom"
                kind = "alpha_cleavage"

            if _is_aromatic_fragment(frag):
                intensity *= 1.25
                if label == "bond cleavage":
                    label = "aromatic-stabilized fragment"

            intensity = _jitter(intensity, rng, 0.9, 1.1)

            peaks.append(
                Peak(
                    mz=_round_mz(mz),
                    intensity=float(intensity),
                    label=label,
                    kind=kind,
                    fragment_smiles=_fragment_smiles(frag),
                    metadata={
                        "heavy_atoms": heavy_atoms,
                        "aromatic": _is_aromatic_fragment(frag),
                        "hetero": _contains_hetero(frag),
                    },
                )
            )

    return peaks


def _generate_second_generation_fragments(
    cleavage_peaks: List[Peak],
    rng: random.Random,
) -> List[Peak]:
    """
    Kontrollierte Fragmentierung von Fragmenten:
    nur starke/stabile Primärfragmente werden einmal weiterfragmentiert.
    """
    peaks: List[Peak] = []

    for peak in cleavage_peaks:
        if peak.intensity < 30:
            continue
        if not peak.fragment_smiles:
            continue

        try:
            frag_mol = _safe_mol_from_smiles(peak.fragment_smiles)
        except ValueError:
            continue

        if frag_mol.GetNumHeavyAtoms() < 4:
            continue

        child_peaks = _generate_cleavage_peaks(frag_mol, rng)
        for child in child_peaks[:4]:
            child.intensity *= 0.45
            child.label = f"secondary fragmentation: {child.label}"
            child.kind = "secondary_fragmentation"
            peaks.append(child)

    return peaks


def _generate_isotope_peaks(features: MoleculeFeatures, parent_peak: Peak) -> List[Peak]:
    peaks: List[Peak] = []

    # M+1: grobe 13C-Regel
    if features.carbon_count > 0:
        m1_intensity = min(parent_peak.intensity * (0.011 * features.carbon_count), 35.0)
        if m1_intensity >= 1.0:
            peaks.append(
                Peak(
                    mz=_round_mz(parent_peak.mz + 1.0034),
                    intensity=m1_intensity,
                    label="M+1",
                    kind="isotope",
                )
            )

    cl_count = features.hetero_counts.get("Cl", 0)
    br_count = features.hetero_counts.get("Br", 0)
    s_count = features.hetero_counts.get("S", 0)

    # Chlor: M:M+2 ≈ 3:1
    if cl_count == 1:
        peaks.append(
            Peak(
                mz=_round_mz(parent_peak.mz + 1.9970),
                intensity=parent_peak.intensity * 0.33,
                label="M+2 (Cl)",
                kind="isotope",
            )
        )
    elif cl_count >= 2:
        peaks.append(
            Peak(
                mz=_round_mz(parent_peak.mz + 1.9970),
                intensity=parent_peak.intensity * 0.66,
                label="M+2 (2×Cl)",
                kind="isotope",
            )
        )
        peaks.append(
            Peak(
                mz=_round_mz(parent_peak.mz + 3.9940),
                intensity=parent_peak.intensity * 0.11,
                label="M+4 (2×Cl)",
                kind="isotope",
            )
        )

    # Brom: M:M+2 ≈ 1:1
    if br_count == 1:
        peaks.append(
            Peak(
                mz=_round_mz(parent_peak.mz + 1.9970),
                intensity=parent_peak.intensity * 0.98,
                label="M+2 (Br)",
                kind="isotope",
            )
        )
    elif br_count >= 2:
        peaks.append(
            Peak(
                mz=_round_mz(parent_peak.mz + 1.9970),
                intensity=parent_peak.intensity * 2.0,
                label="M+2 (2×Br)",
                kind="isotope",
            )
        )
        peaks.append(
            Peak(
                mz=_round_mz(parent_peak.mz + 3.9940),
                intensity=parent_peak.intensity * 1.0,
                label="M+4 (2×Br)",
                kind="isotope",
            )
        )

    # Schwefel: kleines M+2
    if s_count > 0:
        peaks.append(
            Peak(
                mz=_round_mz(parent_peak.mz + 1.9958),
                intensity=parent_peak.intensity * 0.04 * s_count,
                label="M+2 (S)",
                kind="isotope",
            )
        )

    return peaks


def _generate_noise_peaks(
    max_mz: float,
    rng: random.Random,
    count: int = 3,
) -> List[Peak]:
    peaks: List[Peak] = []
    if max_mz < 40:
        return peaks

    for _ in range(count):
        mz = rng.uniform(15, max_mz - 5)
        intensity = rng.uniform(2.0, 8.0)
        peaks.append(
            Peak(
                mz=_round_mz(mz, 2),
                intensity=intensity,
                label="minor signal",
                kind="noise",
            )
        )
    return peaks


# ============================================================
# Peak post-processing
# ============================================================

def _merge_close_peaks(peaks: List[Peak], tolerance: float = 0.35) -> List[Peak]:
    if not peaks:
        return []

    peaks_sorted = sorted(peaks, key=lambda p: p.mz)
    merged: List[Peak] = [peaks_sorted[0]]

    for peak in peaks_sorted[1:]:
        last = merged[-1]
        if abs(last.mz - peak.mz) <= tolerance:
            total_int = last.intensity + peak.intensity
            if total_int <= 0:
                continue

            mz = (last.mz * last.intensity + peak.mz * peak.intensity) / total_int
            label = last.label if last.intensity >= peak.intensity else peak.label
            fragment_smiles = last.fragment_smiles or peak.fragment_smiles

            merged[-1] = Peak(
                mz=_round_mz(mz),
                intensity=total_int,
                label=label,
                kind=last.kind if last.intensity >= peak.intensity else peak.kind,
                fragment_smiles=fragment_smiles,
                metadata={**last.metadata, **peak.metadata},
            )
        else:
            merged.append(peak)

    return merged


def _normalize_peaks(peaks: List[Peak]) -> List[Peak]:
    if not peaks:
        return peaks

    max_int = max(p.intensity for p in peaks)
    if max_int <= 0:
        return peaks

    normalized: List[Peak] = []
    for p in peaks:
        normalized.append(
            Peak(
                mz=p.mz,
                intensity=100.0 * p.intensity / max_int,
                label=p.label,
                kind=p.kind,
                fragment_smiles=p.fragment_smiles,
                metadata=p.metadata,
            )
        )
    return normalized


def _trim_peaks(peaks: List[Peak], max_peaks: int = 22, min_intensity: float = 2.0) -> List[Peak]:
    filtered = [p for p in peaks if p.intensity >= min_intensity]
    filtered.sort(key=lambda p: (-p.intensity, p.mz))
    filtered = filtered[:max_peaks]
    filtered.sort(key=lambda p: p.mz)
    return filtered


# ============================================================
# Public API
# ============================================================

def simulate_ms(smiles: str, seed: int = 42) -> dict:
    """
    Vereinfachte, didaktische MS-Simulation.

    Rückgabeformat:
    {
        "molecular_ion": float,
        "formula": str,
        "features": {...},
        "peaks": [
            {"mz": float, "intensity": float, "label": str}
        ],
        "peak_details": [...]
    }
    """
    rng = random.Random(seed)

    mol = _safe_mol_from_smiles(smiles)
    features = extract_molecule_features(smiles)

    molecular_ion = _generate_molecular_ion_peak(features, rng)
    neutral_losses = _generate_neutral_loss_peaks(features, rng)
    cleavage_peaks = _generate_cleavage_peaks(mol, rng)
    second_gen = _generate_second_generation_fragments(cleavage_peaks, rng)
    isotope_peaks = _generate_isotope_peaks(features, molecular_ion)
    noise_peaks = _generate_noise_peaks(features.exact_mass, rng, count=2)

    all_peaks = [molecular_ion] + neutral_losses + cleavage_peaks + second_gen + isotope_peaks + noise_peaks
    all_peaks = _merge_close_peaks(all_peaks, tolerance=0.35)
    all_peaks = _normalize_peaks(all_peaks)
    all_peaks = _trim_peaks(all_peaks, max_peaks=22, min_intensity=2.0)

    return {
        "molecular_ion": _round_mz(features.exact_mass),
        "formula": features.formula,
        "features": {
            "has_aromatic": features.has_aromatic,
            "has_alcohol": features.has_alcohol,
            "has_phenol": features.has_phenol,
            "has_carboxylic_acid": features.has_carboxylic_acid,
            "has_ester": features.has_ester,
            "has_ketone": features.has_ketone,
            "has_aldehyde": features.has_aldehyde,
            "has_amide": features.has_amide,
            "has_anhydride": features.has_anhydride,
            "has_ether_aliphatic": features.has_ether_aliphatic,
            "has_ether_aromatic": features.has_ether_aromatic,
            "has_epoxide": features.has_epoxide,
            "has_primary_amine": features.has_primary_amine,
            "has_secondary_amine": features.has_secondary_amine,
            "has_tertiary_amine": features.has_tertiary_amine,
            "has_nitrile": features.has_nitrile,
            "has_nitro": features.has_nitro,
            "has_imine": features.has_imine,
            "has_thiol": features.has_thiol,
            "has_thioether": features.has_thioether,
            "has_terminal_alkyne": features.has_terminal_alkyne,
            "has_internal_alkyne": features.has_internal_alkyne,
            "has_alkene": features.has_alkene,
            "has_halogen_cl": features.has_halogen_cl,
            "has_halogen_br": features.has_halogen_br,
            "has_halogen_f": features.has_halogen_f,
            "has_halogen_i": features.has_halogen_i,
            "carbonyl_like": features.carbonyl_like,
        },
        "peaks": [
            {
                "mz": p.mz,
                "intensity": round(p.intensity, 1),
                "label": p.label,
            }
            for p in all_peaks
        ],
        "peak_details": [
            {
                "mz": p.mz,
                "intensity": round(p.intensity, 1),
                "label": p.label,
                "kind": p.kind,
                "fragment_smiles": p.fragment_smiles,
                "metadata": p.metadata,
            }
            for p in all_peaks
        ],
    }


# ============================================================
# Plotting
# ============================================================

def make_interactive_ms_plot(ms_result: dict) -> go.Figure:
    peaks = ms_result.get("peak_details") or ms_result.get("peaks", [])
    if not peaks:
        fig = go.Figure()
        fig.update_layout(
            template="plotly_white",
            xaxis_title="m/z",
            yaxis_title="Intensity (%)",
        )
        return fig

    x_vals: List[float] = []
    y_vals: List[float] = []
    labels: List[str] = []
    kinds: List[str] = []
    frag_smiles: List[str] = []

    for peak in peaks:
        mz = float(peak["mz"])
        intensity = float(peak["intensity"])
        label = str(peak.get("label", ""))
        kind = str(peak.get("kind", ""))
        fragment_smiles = str(peak.get("fragment_smiles") or "")

        # Stick spectrum: je Peak 3 Punkte
        x_vals.extend([mz, mz, None])
        y_vals.extend([0, intensity, None])
        labels.extend([label, label, ""])
        kinds.extend([kind, kind, ""])
        frag_smiles.extend([fragment_smiles, fragment_smiles, ""])

    max_mz = max(float(p["mz"]) for p in peaks)

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=x_vals,
            y=y_vals,
            mode="lines",
            line=dict(width=2),
            hoverinfo="text",
            text=[
                (
                    f"m/z: {x_vals[i]:.4f}<br>"
                    f"Intensity: {y_vals[i]:.1f}%<br>"
                    f"Label: {labels[i]}"
                    + (f"<br>Type: {kinds[i]}" if kinds[i] else "")
                    + (f"<br>Fragment: {frag_smiles[i]}" if frag_smiles[i] else "")
                )
                if x_vals[i] is not None and y_vals[i] is not None and y_vals[i] > 0
                else ""
                for i in range(len(x_vals))
            ],
            showlegend=False,
        )
    )

    # Peak labels für stärkere Peaks
    strong_peaks = [p for p in peaks if float(p["intensity"]) >= 25]
    for p in strong_peaks:
        fig.add_annotation(
            x=float(p["mz"]),
            y=float(p["intensity"]),
            text=p["label"],
            showarrow=False,
            yshift=10,
            font=dict(size=10),
        )

    fig.update_layout(
        xaxis_title="m/z",
        yaxis_title="Intensity (%)",
        hovermode="closest",
        template="plotly_white",
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis=dict(range=[0, math.ceil(max_mz * 1.08)]),
        yaxis=dict(range=[0, 110]),
    )

    return fig