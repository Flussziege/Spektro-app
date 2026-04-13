from __future__ import annotations
from rdkit import Chem
from rdkit.Chem import Draw


def normalize_smiles(smiles: str) -> str:
    return (smiles or "").strip()


def get_display_name(molecule: dict, lang: str = "de") -> str:
    if not isinstance(molecule, dict):
        return str(molecule)

    if lang == "en":
        return (
            molecule.get("name_en")
            or molecule.get("name_de")
            or molecule.get("name")
            or "Unknown"
        )

    return (
        molecule.get("name_de")
        or molecule.get("name_en")
        or molecule.get("name")
        or "Unbekannt"
    )


def get_difficulty(molecule: dict, default: str = "medium") -> str:
    difficulty = (molecule.get("difficulty") or default).strip().lower()
    if difficulty not in {"easy", "medium", "hard"}:
        return default
    return difficulty


def build_name_maps(molecules: list[dict], lang: str = "de"):
    names: list[str] = []
    name_to_smiles: dict[str, str] = {}
    smiles_to_name: dict[str, str] = {}

    for m in molecules:
        display_name = get_display_name(m, lang).strip()
        smiles = normalize_smiles(m.get("smiles", ""))

        if not display_name or not smiles:
            continue

        names.append(display_name)
        name_to_smiles[display_name.lower()] = smiles

        if smiles not in smiles_to_name:
            smiles_to_name[smiles] = display_name

    return names, name_to_smiles, smiles_to_name


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