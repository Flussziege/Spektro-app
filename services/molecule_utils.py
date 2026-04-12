from __future__ import annotations
import io
from rdkit import Chem
from rdkit.Chem import Draw


def build_name_maps(molecules: list[dict]) -> tuple[list[str], dict[str, str], dict[str, str]]:
    names = [m["name"] for m in molecules]
    name_to_smiles = {m["name"].strip().lower(): m["smiles"] for m in molecules}
    smiles_to_name = {m["smiles"].strip().lower(): m["name"] for m in molecules}
    return names, name_to_smiles, smiles_to_name


def smiles_to_pil(smiles: str, size=(350, 350)):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    return Draw.MolToImage(mol, size=size)


def molecule_exists(smiles: str) -> bool:
    return Chem.MolFromSmiles(smiles) is not None
