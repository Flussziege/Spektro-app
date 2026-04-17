from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple
import math
import random

from rdkit import Chem
from rdkit.Chem import Descriptors, rdMolDescriptors


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
    has_aromatic_carbonyl: bool = False

    carbonyl_like: bool = False

    aromatic_atom_count: int = 0
    has_benzylic_position: bool = False
    has_benzene_like_ring: bool = False
    has_aromatic_seven_ring: bool = False


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
    "carbonyl_cc": "[CX3](=O)[#6]",
    "carbonyl_any": "[CX3](=O)",
    "aryl_carbonyl": "c[CX3](=O)",
    "cyclohexene_like": "[#6]1~[#6]~[#6]=[#6]~[#6]~[#6]1",
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


def _count_aromatic_atoms(mol: Chem.Mol) -> int:
    return sum(1 for atom in mol.GetAtoms() if atom.GetIsAromatic())


def _has_benzylic_position(mol: Chem.Mol) -> bool:
    for atom in mol.GetAtoms():
        if atom.GetAtomicNum() != 6:
            continue
        if atom.GetHybridization() != Chem.rdchem.HybridizationType.SP3:
            continue
        if atom.GetIsAromatic():
            continue
        aromatic_neighbors = [nbr for nbr in atom.GetNeighbors() if nbr.GetIsAromatic()]
        if not aromatic_neighbors:
            continue
        return True
    return False


def _has_benzene_like_ring(mol: Chem.Mol) -> bool:
    ring_info = mol.GetRingInfo()
    for ring in ring_info.AtomRings():
        if len(ring) == 6 and all(mol.GetAtomWithIdx(idx).GetIsAromatic() for idx in ring):
            return True
    return False


def _is_benzene_like(fragment: Chem.Mol) -> bool:
    if fragment.GetNumAtoms() != 6:
        return False
    return all(atom.GetIsAromatic() for atom in fragment.GetAtoms())


def _has_aromatic_seven_membered_ring(mol: Chem.Mol) -> bool:
    ring_info = mol.GetRingInfo()
    for ring in ring_info.AtomRings():
        if len(ring) != 7:
            continue
        aromatic_atoms = sum(1 for idx in ring if mol.GetAtomWithIdx(idx).GetIsAromatic())
        if aromatic_atoms >= 5:
            return True
    return False


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
        aromatic_atom_count=_count_aromatic_atoms(mol),
        has_benzylic_position=_has_benzylic_position(mol),
        has_benzene_like_ring=_has_benzene_like_ring(mol),
        has_aromatic_seven_ring=_has_aromatic_seven_membered_ring(mol),
        has_aromatic_carbonyl=_has_substructure(mol, "aryl_carbonyl"),
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
    cleavable: List[Chem.Bond] = []

    allowed_pairs = {
        (6, 6), (6, 7), (7, 6), (6, 8), (8, 6),
        (6, 16), (16, 6), (7, 8), (8, 7),
    }

    for bond in mol.GetBonds():
        if bond.GetBondType() != Chem.rdchem.BondType.SINGLE:
            continue
        if bond.IsInRing():
            continue

        a1 = bond.GetBeginAtom()
        a2 = bond.GetEndAtom()

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
    score = 1.0

    aromatic_atoms = _count_aromatic_atoms(fragment)
    if aromatic_atoms > 0:
        score += 0.5 + 0.05 * aromatic_atoms

    if _contains_hetero(fragment):
        score += 0.25

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
            if any(
                nbr.GetAtomicNum() in (7, 8, 16) and nbr.GetIdx() != other.GetIdx()
                for nbr in atom.GetNeighbors()
            ):
                return True

    return False

def _iter_carbonyl_carbons(mol: Chem.Mol):
    for atom in mol.GetAtoms():
        if atom.GetAtomicNum() != 6:
            continue
        for bond in atom.GetBonds():
            if (
                bond.GetBondType() == Chem.rdchem.BondType.DOUBLE
                and bond.GetOtherAtom(atom).GetAtomicNum() == 8
            ):
                yield atom
                break


def _fragment_has_true_carbonyl(fragment: Chem.Mol) -> bool:
    patt = COMPILED_SMARTS.get("carbonyl_any")
    return bool(patt and fragment.HasSubstructMatch(patt))


def _is_carbonyl_like_fragment(fragment: Chem.Mol) -> bool:
    return any(
        _has_substructure(fragment, key)
        for key in (
            "carboxylic_acid",
            "ester",
            "ketone",
            "aldehyde",
            "amide",
            "anhydride",
        )
    )


def _has_allylic_position(mol: Chem.Mol) -> bool:
    for atom in mol.GetAtoms():
        if atom.GetAtomicNum() != 6:
            continue
        if atom.GetIsAromatic():
            continue
        if atom.GetHybridization() != Chem.rdchem.HybridizationType.SP3:
            continue

        for nbr in atom.GetNeighbors():
            bond = mol.GetBondBetweenAtoms(atom.GetIdx(), nbr.GetIdx())
            if bond is None or bond.GetBondType() != Chem.rdchem.BondType.SINGLE:
                continue
            if nbr.GetAtomicNum() != 6 or nbr.GetIsAromatic():
                continue

            for nbr2 in nbr.GetNeighbors():
                if nbr2.GetIdx() == atom.GetIdx():
                    continue
                bond2 = mol.GetBondBetweenAtoms(nbr.GetIdx(), nbr2.GetIdx())
                if bond2 is not None and bond2.GetBondType() == Chem.rdchem.BondType.DOUBLE:
                    return True
    return False


def _count_tertiary_carbon_centers(mol: Chem.Mol) -> int:
    count = 0
    for atom in mol.GetAtoms():
        if atom.GetAtomicNum() != 6 or atom.GetIsAromatic():
            continue
        if _count_carbon_neighbors(atom) >= 3:
            count += 1
    return count


def _is_acylium_like_fragment(fragment: Chem.Mol) -> bool:
    if not _fragment_has_true_carbonyl(fragment):
        return False

    o_count = _count_atoms(fragment, 8)
    if o_count == 0 or o_count > 2:
        return False

    heavy_atoms = fragment.GetNumHeavyAtoms()
    if heavy_atoms > 8 and not _is_aromatic_fragment(fragment):
        return False

    for atom in fragment.GetAtoms():
        if atom.GetAtomicNum() != 6:
            continue
        carbonyl_oxygen_found = False
        carbon_or_n_neighbor = False

        for bond in atom.GetBonds():
            other = bond.GetOtherAtom(atom)
            if bond.GetBondType() == Chem.rdchem.BondType.DOUBLE and other.GetAtomicNum() == 8:
                carbonyl_oxygen_found = True
            elif other.GetAtomicNum() in (6, 7):
                carbon_or_n_neighbor = True

        if carbonyl_oxygen_found and carbon_or_n_neighbor:
            return True

    return False


def _estimate_cation_preference(fragment: Chem.Mol) -> float:
    score = 1.0

    aromatic_atoms = _count_aromatic_atoms(fragment)
    if aromatic_atoms:
        score += 0.18 + 0.07 * aromatic_atoms

    if _has_benzylic_position(fragment):
        score += 0.25

    if _has_allylic_position(fragment):
        score += 0.18

    tertiary_centers = _count_tertiary_carbon_centers(fragment)
    if tertiary_centers:
        score += min(0.30, 0.12 + 0.10 * tertiary_centers)

    n_count = _count_atoms(fragment, 7)
    if n_count:
        score += 0.12 + 0.08 * min(n_count, 2)

    if _has_substructure(fragment, "tertiary_amine"):
        score += 0.15
    elif _has_substructure(fragment, "secondary_amine"):
        score += 0.08

    if _fragment_has_true_carbonyl(fragment):
        score += 0.10

    if _is_acylium_like_fragment(fragment):
        score += 0.35

    heavy_atoms = fragment.GetNumHeavyAtoms()
    if heavy_atoms <= 2:
        score *= 0.82
    elif heavy_atoms <= 4:
        score *= 0.92

    return max(0.70, min(2.30, score))


def _collect_carbonyl_fragment_candidates(mol: Chem.Mol) -> List[Chem.Mol]:
    candidates: List[Chem.Mol] = []
    seen: set = set()

    for carbonyl_c in _iter_carbonyl_carbons(mol):
        for nbr in carbonyl_c.GetNeighbors():
            if nbr.GetAtomicNum() not in (6, 7):
                continue

            bond = mol.GetBondBetweenAtoms(carbonyl_c.GetIdx(), nbr.GetIdx())
            if bond is None:
                continue
            if bond.GetBondType() != Chem.rdchem.BondType.SINGLE:
                continue
            if bond.IsInRing():
                continue

            try:
                frags = _split_molecule_on_bond(mol, bond.GetIdx())
            except Exception:
                continue

            for frag in frags:
                if not _fragment_has_true_carbonyl(frag):
                    continue

                smiles = _fragment_smiles(frag)
                if smiles in seen:
                    continue
                seen.add(smiles)
                candidates.append(frag)

    return candidates


def _collect_ester_alkoxy_fragments(mol: Chem.Mol) -> List[Chem.Mol]:
    patt = COMPILED_SMARTS.get("ester")
    if patt is None:
        return []

    frags_out: List[Chem.Mol] = []
    seen: set = set()

    for match in mol.GetSubstructMatches(patt):
        if len(match) < 3:
            continue
        o_idx = match[1]
        alkyl_idx = match[2]

        bond = mol.GetBondBetweenAtoms(o_idx, alkyl_idx)
        if bond is None or bond.IsInRing():
            continue

        try:
            frags = _split_molecule_on_bond(mol, bond.GetIdx())
        except Exception:
            continue

        for frag in frags:
            if _fragment_has_true_carbonyl(frag):
                continue
            if _count_atoms(frag, 8) == 0:
                continue
            if frag.GetNumHeavyAtoms() > 6:
                continue

            smiles = _fragment_smiles(frag)
            if smiles in seen:
                continue
            seen.add(smiles)
            frags_out.append(frag)

    return frags_out


# ============================================================
# Peak generation
# ============================================================

def _generate_molecular_ion_peak(features: MoleculeFeatures, rng: random.Random) -> Peak:
    intensity = 20.0

    if features.has_aromatic:
        intensity += 10
    if features.has_benzene_like_ring:
        intensity += 5
    if features.has_benzylic_position:
        intensity += 4
    if features.has_aromatic_seven_ring:
        intensity += 7
    if features.carbonyl_like:
        intensity += 6
    if features.has_halogen_cl or features.has_halogen_br:
        intensity += 5

    # differenziertere Carbonyl-Familien
    if features.has_amide:
        intensity += 9
    if features.has_carboxylic_acid:
        intensity += 4
    if features.has_ester:
        intensity += 2
    if features.has_aldehyde:
        intensity -= 2

    if not features.has_aromatic and not features.carbonyl_like and features.carbon_count >= 5:
        intensity -= 8

    if features.hetero_counts["N"] >= 2:
        intensity *= 0.80
    elif features.hetero_counts["N"] == 0 and not features.has_aromatic:
        intensity *= 0.85

    intensity = max(8.0, min(55.0, _jitter(intensity, rng, 0.9, 1.1)))

    return Peak(
        mz=_round_mz(features.exact_mass),
        intensity=intensity,
        label="M⁺",
        kind="molecular_ion",
    )


def _generate_aromatic_special_peaks(
    mol: Chem.Mol,
    features: MoleculeFeatures,
    rng: random.Random,
) -> List[Peak]:
    peaks: List[Peak] = []

    if not features.has_aromatic or not features.has_benzene_like_ring:
        return peaks

    # Aromatische Carbonylverbindungen: kein 91er-Tropylium als Standarddiagnostik
    if features.has_aromatic_carbonyl:
        peaks.extend(
            [
                Peak(
                    mz=_round_mz(77.0391),
                    intensity=_jitter(76.0, rng, 0.90, 1.10),
                    label="phenyl fragment",
                    kind="aromatic_special",
                    metadata={"protected": True},
                ),
                Peak(
                    mz=_round_mz(51.0230),
                    intensity=_jitter(46.0, rng, 0.88, 1.12),
                    label="ring contraction fragment",
                    kind="aromatic_special",
                    metadata={"protected": True},
                ),
                Peak(
                    mz=_round_mz(39.0230),
                    intensity=_jitter(30.0, rng, 0.88, 1.12),
                    label="small aromatic fragment",
                    kind="aromatic_special",
                    metadata={"protected": True},
                ),
            ]
        )
        return peaks

    if features.has_benzylic_position:
        peaks.extend(
            [
                Peak(
                    mz=_round_mz(91.0542),
                    intensity=_jitter(82.0, rng, 0.92, 1.08),
                    label="tropylium / benzyl fragment",
                    kind="aromatic_special",
                    metadata={"protected": True},
                ),
                Peak(
                    mz=_round_mz(65.0386),
                    intensity=_jitter(50.0, rng, 0.90, 1.10),
                    label="benzyl-derived ring fragment",
                    kind="aromatic_special",
                    metadata={"protected": True},
                ),
                Peak(
                    mz=_round_mz(39.0230),
                    intensity=_jitter(30.0, rng, 0.88, 1.12),
                    label="small aromatic fragment",
                    kind="aromatic_special",
                    metadata={"protected": True},
                ),
            ]
        )
        return peaks

    peaks.extend(
        [
            Peak(
                mz=_round_mz(77.0391),
                intensity=_jitter(73.0, rng, 0.90, 1.10),
                label="phenyl fragment",
                kind="aromatic_special",
                metadata={"protected": True},
            ),
            Peak(
                mz=_round_mz(51.0230),
                intensity=_jitter(52.0, rng, 0.88, 1.12),
                label="ring contraction fragment",
                kind="aromatic_special",
                metadata={"protected": True},
            ),
            Peak(
                mz=_round_mz(39.0230),
                intensity=_jitter(40.0, rng, 0.88, 1.12),
                label="small aromatic fragment",
                kind="aromatic_special",
                metadata={"protected": True},
            ),
        ]
    )

    return peaks


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

    if features.carbon_count >= 2:
        base = 24.0
        if features.has_ether_aliphatic or features.has_ester:
            base += 10.0
        add_loss(15.0235, "M−15 (CH₃)", base)

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
            mz = _fragment_mass(frag)

            if heavy_atoms < 2 and mz < 20:
                continue
            if mz < 10:
                continue

            stability = _estimate_fragment_stability(frag)
            cation_pref = _estimate_cation_preference(frag)
            intensity = 16.0 * stability * cation_pref

            label = "bond cleavage"
            kind = "cleavage"

            if alpha_to_hetero:
                intensity *= 1.45
                label = "α-cleavage next to heteroatom"
                kind = "alpha_cleavage"

            if _is_aromatic_fragment(frag):
                intensity *= 1.18
                if label == "bond cleavage":
                    label = "aromatic-stabilized fragment"

            if _is_benzene_like(frag):
                continue

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
                        "cation_preference": round(cation_pref, 3),
                    },
                )
            )

    return peaks



def _generate_second_generation_fragments(
    cleavage_peaks: List[Peak],
    rng: random.Random,
) -> List[Peak]:
    peaks: List[Peak] = []

    sorted_candidates = sorted(cleavage_peaks, key=lambda p: p.intensity, reverse=True)

    for peak in sorted_candidates[:8]:
        aromatic = bool(peak.metadata.get("aromatic"))
        threshold = 22 if aromatic else 30

        if peak.intensity < threshold:
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
        child_peaks = sorted(child_peaks, key=lambda p: p.intensity, reverse=True)[:3]

        for child in child_peaks:
            if child.fragment_smiles:
                try:
                    child_mol = _safe_mol_from_smiles(child.fragment_smiles)
                    child_pref = _estimate_cation_preference(child_mol)
                except ValueError:
                    child_pref = 1.0
            else:
                child_pref = 1.0

            base_factor = 0.52 if aromatic else 0.42
            child.intensity *= base_factor * min(1.45, child_pref)
            child.label = f"secondary fragmentation: {child.label}"
            child.kind = "secondary_fragmentation"
            peaks.append(child)

            if child.fragment_smiles:
                try:
                    child_mol = _safe_mol_from_smiles(child.fragment_smiles)
                except ValueError:
                    continue

                if _has_substructure(child_mol, "alcohol") and child.mz - 18.0106 > 10:
                    peaks.append(Peak(
                        mz=_round_mz(child.mz - 18.0106),
                        intensity=child.intensity * 0.35,
                        label="secondary H₂O loss",
                        kind="secondary_loss",
                    ))

                if _has_substructure(child_mol, "primary_amine") and child.mz - 17.0265 > 10:
                    peaks.append(Peak(
                        mz=_round_mz(child.mz - 17.0265),
                        intensity=child.intensity * 0.30,
                        label="secondary NH₃ loss",
                        kind="secondary_loss",
                    ))

                if _is_carbonyl_like_fragment(child_mol) and child.mz - 27.9949 > 10:
                    peaks.append(Peak(
                        mz=_round_mz(child.mz - 27.9949),
                        intensity=child.intensity * 0.28,
                        label="secondary CO loss",
                        kind="secondary_loss",
                    ))

    return peaks

def _generate_carbonyl_family_peaks(
    mol: Chem.Mol,
    features: MoleculeFeatures,
    rng: random.Random,
) -> List[Peak]:
    if not features.carbonyl_like:
        return []

    peaks: List[Peak] = []
    m = features.exact_mass
    acyl_candidates = sorted(_collect_carbonyl_fragment_candidates(mol), key=_fragment_mass)
    small_acyl_candidates = [
        frag for frag in acyl_candidates
        if 25 <= _fragment_mass(frag) <= 105
    ]

    def add_peak(
        mz: float,
        intensity: float,
        label: str,
        kind: str = "carbonyl_family",
        fragment: Optional[Chem.Mol] = None,
    ) -> None:
        if mz <= 10:
            return

        frag_smiles = _fragment_smiles(fragment) if fragment is not None else None
        metadata = {}
        if fragment is not None:
            metadata = {
                "heavy_atoms": fragment.GetNumHeavyAtoms(),
                "aromatic": _is_aromatic_fragment(fragment),
                "hetero": _contains_hetero(fragment),
            }

        peaks.append(
            Peak(
                mz=_round_mz(mz),
                intensity=_jitter(intensity, rng, 0.90, 1.10),
                label=label,
                kind=kind,
                fragment_smiles=frag_smiles,
                metadata=metadata,
            )
        )

    if features.has_ketone:
        if m - 27.9949 > 10:
            add_peak(m - 27.9949, 44.0, "ketone: CO loss")
        for frag in small_acyl_candidates[:2]:
            pref = _estimate_cation_preference(frag)
            add_peak(
                _fragment_mass(frag),
                38.0 * pref,
                "ketone: small acylium-like fragment",
                fragment=frag,
            )

    if features.has_aldehyde:
        if m - 27.9949 > 10:
            add_peak(m - 27.9949, 34.0, "aldehyde: moderate CO loss")
        if small_acyl_candidates:
            frag = small_acyl_candidates[0]
            pref = _estimate_cation_preference(frag)
            add_peak(
                _fragment_mass(frag),
                24.0 * pref,
                "aldehyde: acyl fragment",
                fragment=frag,
            )

    if features.has_ester:
        if m - 31.0184 > 10:
            add_peak(m - 31.0184, 28.0, "ester: alkoxy loss")
        if m - 45.0335 > 10:
            add_peak(m - 45.0335, 24.0, "ester: alkoxy fragmentation pathway")

        if small_acyl_candidates:
            frag = small_acyl_candidates[0]
            pref = _estimate_cation_preference(frag)
            add_peak(
                _fragment_mass(frag),
                34.0 * pref,
                "ester: acylium pathway",
                fragment=frag,
            )

        alkoxy_frags = _collect_ester_alkoxy_fragments(mol)
        for frag in alkoxy_frags[:2]:
            pref = _estimate_cation_preference(frag)
            add_peak(
                _fragment_mass(frag),
                26.0 * pref,
                "ester: alkoxy fragment",
                fragment=frag,
            )

    if features.has_amide:
        if m - 17.0265 > 10:
            add_peak(m - 17.0265, 18.0, "amide: mild NH₃ loss")
        if small_acyl_candidates:
            frag = small_acyl_candidates[0]
            pref = _estimate_cation_preference(frag)
            add_peak(
                _fragment_mass(frag),
                20.0 * pref,
                "amide: restrained acyl fragment",
                fragment=frag,
            )

    if features.has_carboxylic_acid:
        if m - 43.9898 > 10:
            add_peak(m - 43.9898, 68.0, "acid: strong CO₂ loss")
        if m - 27.9949 > 10:
            add_peak(m - 27.9949, 20.0, "acid: minor CO loss")

    if features.has_anhydride:
        if m - 27.9949 > 10:
            add_peak(m - 27.9949, 42.0, "anhydride: CO loss")
        if m - 43.9898 > 10:
            add_peak(m - 43.9898, 58.0, "anhydride: CO₂ loss")
        if m - 71.9847 > 10:
            add_peak(m - 71.9847, 30.0, "anhydride: sequential CO/CO₂ loss")

    return peaks


def _generate_isotope_peaks(features: MoleculeFeatures, parent_peak: Peak) -> List[Peak]:
    peaks: List[Peak] = []

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

    if cl_count == 1:
        peaks.append(Peak(
            mz=_round_mz(parent_peak.mz + 1.9970),
            intensity=parent_peak.intensity * 0.33,
            label="M+2 (Cl)",
            kind="isotope",
        ))
    elif cl_count >= 2:
        peaks.append(Peak(
            mz=_round_mz(parent_peak.mz + 1.9970),
            intensity=parent_peak.intensity * 0.66,
            label="M+2 (2×Cl)",
            kind="isotope",
        ))
        peaks.append(Peak(
            mz=_round_mz(parent_peak.mz + 3.9940),
            intensity=parent_peak.intensity * 0.11,
            label="M+4 (2×Cl)",
            kind="isotope",
        ))

    if br_count == 1:
        peaks.append(Peak(
            mz=_round_mz(parent_peak.mz + 1.9970),
            intensity=parent_peak.intensity * 0.98,
            label="M+2 (Br)",
            kind="isotope",
        ))
    elif br_count >= 2:
        peaks.append(Peak(
            mz=_round_mz(parent_peak.mz + 1.9970),
            intensity=parent_peak.intensity * 2.0,
            label="M+2 (2×Br)",
            kind="isotope",
        ))
        peaks.append(Peak(
            mz=_round_mz(parent_peak.mz + 3.9940),
            intensity=parent_peak.intensity * 1.0,
            label="M+4 (2×Br)",
            kind="isotope",
        ))

    if s_count > 0:
        peaks.append(Peak(
            mz=_round_mz(parent_peak.mz + 1.9958),
            intensity=parent_peak.intensity * 0.04 * s_count,
            label="M+2 (S)",
            kind="isotope",
        ))

    return peaks


def _generate_noise_peaks(
    max_mz: float,
    rng: random.Random,
    count: int = 3,  # NEW v2: erhöht von 2 auf 4
) -> List[Peak]:
    """
    NEW v2: Exponentialverteiltes Rauschen — mehr Peaks bei niedrigem m/z,
    was echten EI-Spektren näher kommt.
    """
    peaks: List[Peak] = []
    if max_mz < 40:
        return peaks

    for _ in range(count):
        # Exponential-artige Verteilung: häuft sich bei niedrigen m/z
        mz = rng.expovariate(1.0 / (max_mz * 0.12)) + 14.0
        mz = min(mz, max_mz * 0.45)  # kein Rauschen nahe M⁺
        intensity = rng.uniform(1.5, 5.5)
        peaks.append(
            Peak(
                mz=_round_mz(mz, 1),
                intensity=intensity,
                label="minor signal",
                kind="noise",
            )
        )
    return peaks


# ============================================================
# NEW v2: Alkyl-Ionen-Serie
# ============================================================

def _generate_alkyl_series(features: MoleculeFeatures, rng: random.Random) -> List[Peak]:
    """
    CₙH₂ₙ₊₁⁺-Serie für rein aliphatische Moleküle (keine Aromaten, keine Carbonyle).
    Charakteristisch für lineare und verzweigte Alkane/Alkohole ohne starke Chromophore.
    m/z: 29 (C₂), 43 (C₃), 57 (C₄), 71 (C₅), 85 (C₆) ...
    """
    if features.has_aromatic or features.carbonyl_like:
        return []
    if features.carbon_count < 5:
        return []

    peaks: List[Peak] = []
    max_n = min(features.carbon_count - 1, 8)

    for n in range(2, max_n + 1):
        mz = 14.01565 * n + 1.00782  # CₙH₂ₙ₊₁
        # Intensität nimmt mit steigendem n ab
        base_intensity = 40.0 / (1.0 + 0.30 * (n - 2))
        intensity = _jitter(base_intensity, rng, 0.80, 1.20)
        peaks.append(
            Peak(
                mz=_round_mz(mz),
                intensity=intensity,
                label=f"C{n}H{2*n+1}⁺ (alkyl series)",
                kind="alkyl_series",
            )
        )

    return peaks


# ============================================================
# NEW v2: Acylium-Kationen
# ============================================================

def _generate_acylium_peaks(mol: Chem.Mol, features: MoleculeFeatures, rng: random.Random) -> List[Peak]:
    if not features.carbonyl_like:
        return []

    peaks: List[Peak] = []
    seen_mz: set = set()

    for frag in _collect_carbonyl_fragment_candidates(mol):
        if not _is_acylium_like_fragment(frag):
            continue

        o_count = _count_atoms(frag, 8)
        heavy_atoms = frag.GetNumHeavyAtoms()
        mz = _fragment_mass(frag)

        # große, unspezifische O-Fragmente vermeiden
        if o_count > 2:
            continue
        if heavy_atoms > 8 and not _is_aromatic_fragment(frag):
            continue
        if mz < 25 or mz > features.exact_mass - 5:
            continue

        mz_key = round(mz, 1)
        if mz_key in seen_mz:
            continue
        seen_mz.add(mz_key)

        cation_pref = _estimate_cation_preference(frag)

        base_intensity = 46.0
        label = "acylium R–C≡O⁺"

        if _is_aromatic_fragment(frag):
            base_intensity += 18.0
            label = "aryl acylium Ar–CO⁺"

        if heavy_atoms <= 4:
            base_intensity += 4.0
        elif heavy_atoms >= 7 and not _is_aromatic_fragment(frag):
            base_intensity -= 8.0

        intensity = _jitter(base_intensity * cation_pref, rng, 0.88, 1.12)

        peaks.append(
            Peak(
                mz=_round_mz(mz),
                intensity=intensity,
                label=label,
                kind="acylium",
                fragment_smiles=_fragment_smiles(frag),
                metadata={
                    "heavy_atoms": heavy_atoms,
                    "aromatic": _is_aromatic_fragment(frag),
                    "hetero": _contains_hetero(frag),
                    "true_carbonyl": True,
                    "cation_preference": round(cation_pref, 3),
                },
            )
        )

    return peaks

#Haloggen muster

def _generate_fragment_isotope_peaks(peaks: List[Peak]) -> List[Peak]:
    isotope_peaks: List[Peak] = []

    for peak in peaks:
        if peak.intensity < 18.0:
            continue
        if not peak.fragment_smiles:
            continue

        try:
            frag = _safe_mol_from_smiles(peak.fragment_smiles)
        except ValueError:
            continue

        cl_count = _count_atoms(frag, 17)
        br_count = _count_atoms(frag, 35)

        if cl_count == 0 and br_count == 0:
            continue

        ratio = 0.33 * cl_count + 1.00 * br_count
        ratio = min(ratio, 2.0)

        isotope_peaks.append(
            Peak(
                mz=_round_mz(peak.mz + 1.9970),
                intensity=peak.intensity * ratio,
                label="fragment M+2 (halogen)",
                kind="isotope",
                metadata={"source_kind": peak.kind},
            )
        )

    return isotope_peaks

# ============================================================
# NEW v2: Retro-Diels-Alder
# ============================================================

def _generate_retro_da_peaks(mol: Chem.Mol, features: MoleculeFeatures, rng: random.Random) -> List[Peak]:
    """
    Retro-Diels-Alder-Fragmentierung für Cyclohexen-artige Ringe.
    Charakteristischer Verlust von Butadien (54 Da) und Ethen (28 Da).
    """
    if features.exact_mass < 80:
        return []

    patt = COMPILED_SMARTS.get("cyclohexene_like")
    if patt is None or not mol.HasSubstructMatch(patt):
        return []

    peaks: List[Peak] = []
    m = features.exact_mass

    # Butadien-Verlust: -54.0470 Da (C₄H₆)
    mz_butadiene = m - 54.0470
    if mz_butadiene > 10:
        peaks.append(Peak(
            mz=_round_mz(mz_butadiene),
            intensity=_jitter(60.0, rng, 0.88, 1.12),
            label="Retro-Diels-Alder (−C₄H₆, 54 Da)",
            kind="retro_da",
        ))

    # Ethen-Verlust: -28.0313 Da (C₂H₄) — schwächer
    mz_ethene = m - 28.0313
    if mz_ethene > 10:
        peaks.append(Peak(
            mz=_round_mz(mz_ethene),
            intensity=_jitter(35.0, rng, 0.85, 1.15),
            label="Retro-Diels-Alder (−C₂H₄, 28 Da)",
            kind="retro_da",
        ))

    return peaks


# ============================================================
# NEW v2: Intensitäts-Kompetition
# ============================================================

def _apply_intensity_competition(peaks: List[Peak]) -> List[Peak]:
    if not peaks:
        return peaks

    exempt_kinds = {"noise", "isotope"}

    active = [
        p for p in peaks
        if p.kind not in exempt_kinds and not p.metadata.get("protected")
    ]
    if not active:
        return peaks

    dominant_intensity = max(p.intensity for p in active)
    weak_threshold = 0.25 * dominant_intensity

    reduction_by_kind = {
        "cleavage": 0.55,
        "alpha_cleavage": 0.60,
        "secondary_fragmentation": 0.52,
        "secondary_loss": 0.72,
        "neutral_loss": 0.78,
        "carbonyl_family": 0.88,
        "acylium": 0.92,
        "aromatic_special": 0.95,
        "retro_da": 0.92,
        "alkyl_series": 0.90,
        "molecular_ion": 0.90,
    }

    result: List[Peak] = []
    for p in peaks:
        if (
            p.kind in exempt_kinds
            or p.metadata.get("protected")
            or p.intensity >= weak_threshold
        ):
            result.append(p)
            continue

        factor = reduction_by_kind.get(p.kind, 0.75)
        result.append(
            Peak(
                mz=p.mz,
                intensity=p.intensity * factor,
                label=p.label,
                kind=p.kind,
                fragment_smiles=p.fragment_smiles,
                metadata=p.metadata,
            )
        )

    return result

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


def _trim_peaks(peaks: List[Peak], max_peaks: int = 25, min_intensity: float = 2.0) -> List[Peak]:
    extreme_min = 0.5

    # extreme Ausnahmen immer raus
    peaks = [p for p in peaks if p.intensity >= extreme_min]

    protected = [p for p in peaks if p.metadata.get("protected") is True]
    regular = [p for p in peaks if not p.metadata.get("protected")]

    # geschützte Peaks bleiben erhalten, auch wenn sie unter min_intensity liegen
    regular = [p for p in regular if p.intensity >= min_intensity]

    protected.sort(key=lambda p: (-p.intensity, p.mz))
    regular.sort(key=lambda p: (-p.intensity, p.mz))

    # nur die nicht-geschützten Peaks werden begrenzt
    remaining_slots = max(0, max_peaks - len(protected))
    trimmed = protected + regular[:remaining_slots]

    trimmed.sort(key=lambda p: p.mz)
    return trimmed

# ============================================================
# Public API
# ============================================================

def simulate_ms(smiles: str, seed: int = 42) -> dict:
    rng = random.Random(seed)

    mol = _safe_mol_from_smiles(smiles)
    features = extract_molecule_features(smiles)

    if features.carbon_count <= 6:
        noise_count = 2
    elif features.carbon_count <= 12:
        noise_count = 3
    else:
        noise_count = 4

    molecular_ion = _generate_molecular_ion_peak(features, rng)
    neutral_losses = _generate_neutral_loss_peaks(features, rng)
    cleavage_peaks = _generate_cleavage_peaks(mol, rng)
    second_gen = _generate_second_generation_fragments(cleavage_peaks, rng)
    isotope_peaks = _generate_isotope_peaks(features, molecular_ion)
    noise_peaks = _generate_noise_peaks(features.exact_mass, rng, count=noise_count)
    aromatic_specials = _generate_aromatic_special_peaks(mol, features, rng)

    alkyl_series = _generate_alkyl_series(features, rng)
    acylium_peaks = _generate_acylium_peaks(mol, features, rng)
    retro_da_peaks = _generate_retro_da_peaks(mol, features, rng)
    carbonyl_family_peaks = _generate_carbonyl_family_peaks(mol, features, rng)

    all_peaks = (
        [molecular_ion]
        + neutral_losses
        + cleavage_peaks
        + aromatic_specials
        + second_gen
        + isotope_peaks
        + noise_peaks
        + alkyl_series
        + acylium_peaks
        + retro_da_peaks
        + carbonyl_family_peaks
    )

    all_peaks = _apply_intensity_competition(all_peaks)

    # Fragment-Isotopenmuster nach Hauptgenerierung ergänzen
    fragment_isotopes = _generate_fragment_isotope_peaks(all_peaks)
    all_peaks.extend(fragment_isotopes)

    all_peaks = _merge_close_peaks(all_peaks, tolerance=0.35)
    all_peaks = _normalize_peaks(all_peaks)
    all_peaks = _trim_peaks(all_peaks, max_peaks=25, min_intensity=2.0)

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