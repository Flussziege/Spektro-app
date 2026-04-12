from rdkit import Chem
from rdkit.Chem import rdMolDescriptors
from collections import Counter

def elementaranalyse(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None

    mol_h = Chem.AddHs(mol)
    mol_weight = rdMolDescriptors.CalcExactMolWt(mol)

    atom_masses = {
        "H": 1.0079,
        "C": 12.011,
        "N": 14.007,
        "O": 15.999,
        "S": 32.065,
        "Cl": 35.45,
        "Br": 79.904,
    }

    counts = Counter(atom.GetSymbol() for atom in mol_h.GetAtoms())

    analysis = {}
    for el, count in counts.items():
        mass = atom_masses.get(el, 0) * count
        percent = (mass / mol_weight) * 100
        analysis[el] = percent

    return analysis