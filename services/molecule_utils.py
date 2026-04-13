from __future__ import annotations
from rdkit import Chem
from rdkit.Chem import Draw


def get_display_name(molecule: dict, lang: str = "de") -> str:
    if lang == "en":
        return molecule.get("name_en", molecule.get("name_de", "Unknown"))
    return molecule.get("name_de", molecule.get("name_en", "Unbekannt"))


def build_name_maps(molecules: list[dict], lang: str = "de"):
    if lang == "en":
        names = [m["name_en"] for m in molecules]
        name_to_smiles = {
            m["name_en"].strip().lower(): m["smiles"]
            for m in molecules
        }
    else:
        names = [m["name_de"] for m in molecules]
        name_to_smiles = {
            m["name_de"].strip().lower(): m["smiles"]
            for m in molecules
        }

    smiles_to_name = {}
    for m in molecules:
        display_name = get_display_name(m, lang)
        smiles_to_name[m["smiles"].strip().lower()] = display_name

    return names, name_to_smiles, smiles_to_name


def build_smiles_to_molecule_map(molecules: list[dict]) -> dict[str, dict]:
    return {m["smiles"].strip().lower(): m for m in molecules}


def smiles_to_pil(smiles: str, size=(350, 350)):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    return Draw.MolToImage(mol, size=size)


def molecule_exists(smiles: str) -> bool:
    return Chem.MolFromSmiles(smiles) is not None