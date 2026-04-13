from __future__ import annotations

def get_text(lang: str, key: str, **kwargs) -> str:
    text = TEXTS.get(lang, TEXTS["de"]).get(key, key)
    if kwargs:
        return text.format(**kwargs)
    return text

TEXTS = {
    "de": {
        "page_title": "Spektren Quiz",
        "language_label": "Sprache",
        "lang_de": "Deutsch",
        "lang_en": "Englisch",

        "home_title": "Spektren Quiz",
        "home_subtitle": "Trainiere die Zuordnung organischer Moleküle anhand simulierter Spektren.",

        "card_quiz_title": "Quiz",
        "card_quiz_text": "Zufälliges Molekül aus der Hauptliste.",

        "card_daily_title": "Daily Quiz",
        "card_daily_text": "Jeden Tag ein neues Molekül.",

        "quiz_start": "Quiz starten",
        "daily_open": "Daily Quiz öffnen",

        "lookup_expander": "Molekül nachschlagen",
        "lookup_name": "Name auswählen",
        "lookup_smiles": "Oder SMILES eingeben",
        "lookup_submit": "Nachschlagen",
        "lookup_title": "Molekül nachschlagen",
        "lookup_empty": "Kein Molekül ausgewählt.",

        "invalid_smiles": "Ungültiger SMILES.",
        "lookup_missing_input": "Bitte Namen auswählen oder SMILES eingeben.",

        "quiz_title": "Quiz",
        "quiz_question": "Welches Molekül ist das?",
        "quiz_submit": "Abgeben",
        "daily_submit": "Daily abgeben",
        "back_home": "Zur Startseite",
        "startpage": "Startseite",
        "another_quiz": "Noch ein Quiz",

        "daily_title": "Daily Quiz",
        "daily_question": "Welches Molekül ist das heute?",
        "daily_done": "Du hast das Daily Quiz heute bereits abgeschlossen.",

        "no_quiz_active": "Kein Quiz aktiv.",
        "no_lookup_selected": "Kein Molekül ausgewählt.",

        "correct_quiz": "Richtig. Das Molekül war **{name}**.",
        "wrong_quiz": "Falsch. Richtig war **{name}**.",
        "correct_daily": "Richtig. Das heutige Molekül war **{name}**.",
        "wrong_daily": "Falsch. Das heutige Molekül war **{name}**.",

        "correct_label": "Richtig: {name}",
        "your_answer_label": "Deine Antwort: {name}",
        "no_answer_image": "Kein Molekülbild für die Antwort verfügbar.",

        "ea_title": "Elementaranalyse",
        "ea_missing": "Keine EA-Daten verfügbar.",
        "ea_error": "EA konnte nicht berechnet werden: {error}",

        "structure_title": "Struktur",
        "structure_missing": "Strukturbild konnte nicht erzeugt werden.",
        "structure_error": "Struktur konnte nicht gezeichnet werden: {error}",
        "structure_display_error": "Struktur konnte nicht angezeigt werden: {error}",

        "c13_nmr_title": "13C NMR",
        "h1_nmr_title": "1H NMR",
        "ir_title": "IR",
        "no_selection": "Keine Auswahl",
        "difficulty_label": "Schwierigkeit",
        "difficulty_easy": "Leicht",
        "difficulty_medium": "Mittel",
        "difficulty_hard": "Schwer",

        "disclaimer": (
            "Diese Anwendung dient der didaktischen Simulation chemischer Spektren. "
            "Die dargestellten Daten sind modellbasiert und ersetzen keine experimentellen Messdaten. "
            "Es wird keine Gewähr für Richtigkeit oder Vollständigkeit übernommen.\n\n"
            "Kontakt: dailyspectroquizz@gmail.com"
        ),
    },

    "en": {
        "page_title": "Spectra Quiz",
        "language_label": "Language",
        "lang_de": "German",
        "lang_en": "English",

        "home_title": "Spectra Quiz",
        "home_subtitle": "Train assigning organic molecules based on simulated spectra.",

        "card_quiz_title": "Quiz",
        "card_quiz_text": "Random molecule from the main list.",

        "card_daily_title": "Daily Quiz",
        "card_daily_text": "A new molecule every day.",

        "quiz_start": "Start quiz",
        "daily_open": "Open daily quiz",

        "lookup_expander": "Look up molecule",
        "lookup_name": "Select name",
        "lookup_smiles": "Or enter SMILES",
        "lookup_submit": "Look up",
        "lookup_title": "Look up molecule",
        "lookup_empty": "No molecule selected.",

        "invalid_smiles": "Invalid SMILES.",
        "lookup_missing_input": "Please select a name or enter a SMILES string.",

        "quiz_title": "Quiz",
        "quiz_question": "Which molecule is this?",
        "quiz_submit": "Submit",
        "daily_submit": "Submit daily quiz",
        "back_home": "Back to home",
        "startpage": "Home",
        "another_quiz": "Another quiz",

        "daily_title": "Daily Quiz",
        "daily_question": "Which molecule is today’s molecule?",
        "daily_done": "You have already completed today’s daily quiz.",

        "no_quiz_active": "No active quiz.",
        "no_lookup_selected": "No molecule selected.",

        "correct_quiz": "Correct. The molecule was **{name}**.",
        "wrong_quiz": "Incorrect. The correct molecule was **{name}**.",
        "correct_daily": "Correct. Today’s molecule was **{name}**.",
        "wrong_daily": "Incorrect. Today’s molecule was **{name}**.",

        "correct_label": "Correct: {name}",
        "your_answer_label": "Your answer: {name}",
        "no_answer_image": "No molecule image available for this answer.",

        "ea_title": "Elemental analysis",
        "ea_missing": "No elemental analysis data available.",
        "ea_error": "Elemental analysis could not be calculated: {error}",

        "structure_title": "Structure",
        "structure_missing": "Structure image could not be generated.",
        "structure_error": "Structure could not be drawn: {error}",
        "structure_display_error": "Structure could not be displayed: {error}",

        "difficulty_label": "Difficulty",
    "difficulty_easy": "Easy",
    "difficulty_medium": "Medium",
    "difficulty_hard": "Hard",

        "c13_nmr_title": "13C NMR",
        "h1_nmr_title": "1H NMR",
        "ir_title": "IR",
        "no_selection": "No selection",

        "disclaimer": (
            "This application is intended for educational simulation of chemical spectra. "
            "The displayed data are model-based and do not replace experimental measurements. "
            "No guarantee is given for correctness or completeness.\n\n"
            "Contact: dailyspectroquizz@gmail.com"
        ),
    },
}