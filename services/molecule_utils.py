from __future__ import annotations
from rdkit import Chem
from rdkit.Chem import Draw


def normalize_smiles(smiles: str) -> str:
    return (smiles or "").strip()


def get_display_names(molecule: dict, lang: str = "de") -> list[str]:
    if not isinstance(molecule, dict):
        return [str(molecule)]

    if lang == "en":
        candidates = [
            molecule.get("name_en"),
            molecule.get("name_de"),
            molecule.get("name"),
        ]
    else:
        candidates = [
            molecule.get("name_de"),
            molecule.get("name_en"),
            molecule.get("name"),
        ]

    for value in candidates:
        if isinstance(value, str) and value.strip():
            return [value.strip()]

        if isinstance(value, list):
            cleaned = [str(v).strip() for v in value if str(v).strip()]
            if cleaned:
                return cleaned

    return ["Unknown" if lang == "en" else "Unbekannt"]


def get_difficulty(molecule: dict, default: str = "medium") -> str:
    difficulty = (molecule.get("difficulty") or default).strip().lower()
    if difficulty not in {"easy", "medium", "hard"}:
        return default
    return difficulty


def build_name_maps(molecules: list[dict], lang: str = "de"):
    names: list[str] = []
    name_to_smiles: dict[str, str] = {}
    smiles_to_names: dict[str, list[str]] = {}

    for m in molecules:
        smiles = normalize_smiles(m.get("smiles", ""))
        if not smiles:
            continue

        raw_names = m.get(f"name_{lang}") or m.get("name") or []

        if isinstance(raw_names, str):
            raw_names = [raw_names]

        clean_names = [str(n).strip() for n in raw_names if str(n).strip()]
        if not clean_names:
            continue

        for name in clean_names:
            names.append(name)
            name_to_smiles[name.lower()] = smiles

        smiles_to_names[smiles] = clean_names

    names = sorted(set(names), key=str.lower)
    return names, name_to_smiles, smiles_to_names


def build_smiles_to_molecule_map(molecules: list[dict]) -> dict[str, dict]:
    result: dict[str, dict] = {}

    for m in molecules:
        smiles = normalize_smiles(m.get("smiles", ""))
        if not smiles:
            continue
        if smiles not in result:
            result[smiles] = m

    return result


def smiles_to_pil(smiles: str, size=(350, 350)):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    return Draw.MolToImage(mol, size=size)


def molecule_exists(smiles: str) -> bool:
    return Chem.MolFromSmiles(smiles) is not None