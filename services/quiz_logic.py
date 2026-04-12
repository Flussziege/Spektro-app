from __future__ import annotations
import random
from datetime import date
from typing import Optional


def pick_random_molecule(molecules: list[dict]) -> dict:
    if not molecules:
        raise ValueError("Molekülliste ist leer.")
    return random.choice(molecules)


def pick_daily_molecule(molecules: list[dict], today: Optional[date] = None) -> dict:
    if not molecules:
        raise ValueError("Daily-Molekülliste ist leer.")
    today = today or date.today()
    index = today.toordinal() % len(molecules)
    return molecules[index]


def is_correct_answer(user_answer: str, correct_smiles: str, name_to_smiles: dict[str, str]) -> bool:
    if not user_answer:
        return False

    guessed_smiles = name_to_smiles.get(user_answer.strip().lower())
    if guessed_smiles is None:
        return False

    return guessed_smiles.lower() == correct_smiles.lower()
