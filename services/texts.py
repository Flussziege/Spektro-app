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
        "ms_title": "MS",
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
        "selected_answer": "Ausgewählte Antwort",
        "correct_answer": "Richtige Antwort",
        "result_title": "Ergebnis",

        "daily_attempts_label": "Fehlversuche: {count}",
        "wrong_guesses_title": "Bisher falsch geraten",
        "empirical_formula_label": "Empirische Formel: {formula}",
        "empirical_formula_n_label": "Empirische Formel als Wiederholungseinheit: {formula}",
        "molecular_formula_label": "Summenformel: {formula}",
        "daily_new_hint_ea": "Neue Hilfe freigeschaltet: Elementaranalyse",
        "daily_new_hint_ms": "Neue Hilfe freigeschaltet: Massenspektrometrie",
        "daily_new_hint_c13_easy": "Neue Hilfe freigeschaltet: vereinfachtes 13C-NMR",
        "daily_new_hint_empirical": "Neue Hilfe freigeschaltet: empirische Formel",
        "daily_new_hint_formula": "Neue Hilfe freigeschaltet: Summenformel",
        "ms_title": "MS",
        "ms_placeholder": "Massenspektrum wird bald eingebunden.",

        "daily_attempts_label": "Fehlversuche: {count}",
        "wrong_guesses_title": "Bisher falsch geraten",
        "empirical_formula_label": "Empirische Formel: {formula}",
        "empirical_formula_n_label": "Empirische Formel als Wiederholungseinheit: {formula}",
        "molecular_formula_label": "Summenformel: {formula}",
        "daily_new_hint_ea": "Neue Hilfe freigeschaltet: Elementaranalyse",
        "daily_new_hint_ms": "Neue Hilfe freigeschaltet: Massenspektrometrie",
        "daily_new_hint_c13_easy": "Neue Hilfe freigeschaltet: vereinfachtes 13C-NMR",
        "daily_new_hint_empirical": "Neue Hilfe freigeschaltet: empirische Formel",
        "daily_new_hint_formula": "Neue Hilfe freigeschaltet: Summenformel",
        "ms_title": "MS",
        "ms_placeholder": "Massenspektrum wird bald eingebunden.",
        "daily_try_again": "Versuche es erneut. Neue Hinweise werden nach Fehlversuchen freigeschaltet.",
        "empirical_formula_n_label_plain": "Empirische Formel",
        "molecular_formula_label_plain": "Summenformel",
        "daily_already_guessed": "Dieses Molekül wurde bereits geraten. Bitte wähle ein anderes.",
        "daily_invalid_selection": "Bitte wähle ein gültiges Molekül aus der Liste.",
        "how_to_play": "❓ Spielhilfe",
        "how_to_play_quiz_title": "So funktioniert das Quiz",
        "how_to_play_daily_title": "So funktioniert das Daily Quiz",

        "help_navigation_title": "Navigation der Spektren",
        "help_navigation_text": (
            "Die Spektren sind interaktiv. Du kannst horizontal hineinzoomen, "
            "mit gedrückter Maustaste verschieben und per Doppelklick die Ansicht zurücksetzen."
        ),

        "help_simulation_title": "Wichtiger Hinweis zu den Spektren",
        "help_simulation_text": (
            "Alle Spektren sind vereinfacht simuliert und können daher ungenau oder fehlerhaft sein. "
            "Wenn dir ein Fehler auffällt, der das Quiz unlösbar macht oder zu falschen Ergebnissen führt, "
            "melde dich bitte per E-Mail an dailyspectroquizz@gmail.com."
        ),

        "help_ea_title": "Elementaranalyse",
        "help_ea_text": (
            "Die Elementaranalyse zeigt alle im Molekül enthaltenen Elemente an."
        ),

        "help_quiz_attempts_title": "Versuche im normalen Quiz",
        "help_quiz_attempts_text": (
            "Im normalen Quiz hast du nur einen Versuch."
        ),

        "help_daily_attempts_title": "Versuche im Daily Quiz",
        "help_daily_attempts_text": (
            "Im Daily Quiz hast du unbegrenzt viele Versuche."
        ),

        "help_1h_title": "1H-NMR",
        "help_1h_quiz_text": (
            "Im 1H-NMR entspricht die Intensität grob der Protonenzahl. "
            "Bei überlappenden Signalen stimmt das jedoch nicht immer exakt."
        ),

        "help_13c_daily_text": (
            "Im 13C-NMR entspricht die Intensität nicht der Anzahl der Kohlenstoffatome. "
            "Erst nach mehreren Fehlversuchen wird eine vereinfachte Darstellung freigeschaltet."
        ),

        "help_daily_hints_title": "Hilfen im Daily Quiz",
        "help_daily_hints_text": (
            "Nach Fehlversuch 1 wird die Elementaranalyse freigeschaltet. "
            "Nach Fehlversuch 2 wird MS freigeschaltet. "
            "Nach Fehlversuch 3 wird das 13C-NMR vereinfacht. "
            "Nach Fehlversuch 4 wird die empirische Formel angezeigt. "
            "Nach Fehlversuch 5 wird die Summenformel angezeigt."
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
        "ms_title": "MS",
        "no_selection": "No selection",

        "disclaimer": (
            "This application is intended for educational simulation of chemical spectra. "
            "The displayed data are model-based and do not replace experimental measurements. "
            "No guarantee is given for correctness or completeness.\n\n"
            "Contact: dailyspectroquizz@gmail.com"
        ),
        "selected_answer": "Selected answer",
        "correct_answer": "Correct answer",
        "result_title": "Result",

        "daily_attempts_label": "Wrong attempts: {count}",
        "wrong_guesses_title": "Wrong guesses so far",
        "empirical_formula_label": "Empirical formula: {formula}",
        "empirical_formula_n_label": "Empirical formula as repeating unit: {formula}",
        "molecular_formula_label": "Molecular formula: {formula}",
        "daily_new_hint_ea": "New hint unlocked: elemental analysis",
        "daily_new_hint_ms": "New hint unlocked: mass spectrometry",
        "daily_new_hint_c13_easy": "New hint unlocked: simplified 13C NMR",
        "daily_new_hint_empirical": "New hint unlocked: empirical formula",
        "daily_new_hint_formula": "New hint unlocked: molecular formula",
        "ms_title": "MS",
        "ms_placeholder": "Mass spectrum will be integrated soon.",
        "daily_try_again": "Try again. New hints unlock after wrong attempts.",

        "empirical_formula_n_label_plain": "Empirical formula",
        "molecular_formula_label_plain": "Molecular formula",
        "daily_already_guessed": "This molecule has already been guessed. Please choose another one.",
        "daily_invalid_selection": "Please choose a valid molecule from the list.",
        "how_to_play": "❓ How to play",
        "how_to_play_quiz_title": "How the quiz works",
        "how_to_play_daily_title": "How the daily quiz works",

        "help_navigation_title": "How to navigate the spectra",
        "help_navigation_text": (
            "The spectra are interactive. You can zoom horizontally, "
            "pan by dragging, and reset the view with a double click."
        ),

        "help_simulation_title": "Important note about the spectra",
        "help_simulation_text": (
            "All spectra are simplified simulations and may therefore be inaccurate or imperfect. "
            "If you notice an error that makes the quiz unsolvable or leads to wrong results, "
            "please contact us at dailyspectroquizz@gmail.com."
        ),

        "help_ea_title": "Elemental analysis",
        "help_ea_text": (
            "The elemental analysis shows all elements contained in the molecule."
        ),

        "help_quiz_attempts_title": "Attempts in the normal quiz",
        "help_quiz_attempts_text": (
            "In the normal quiz, you only have one attempt."
        ),

        "help_daily_attempts_title": "Attempts in the daily quiz",
        "help_daily_attempts_text": (
            "In the daily quiz, you have unlimited attempts."
        ),

        "help_1h_title": "1H NMR",
        "help_1h_quiz_text": (
            "In the 1H NMR spectrum, signal intensity roughly reflects the number of protons. "
            "However, this is not always exact when signals overlap."
        ),

        "help_13c_daily_text": (
            "In the 13C NMR spectrum, intensity does not correspond to the number of carbon atoms. "
            "Only after several wrong attempts will a simplified version be unlocked."
        ),

        "help_daily_hints_title": "Hints in the daily quiz",
        "help_daily_hints_text": (
            "After wrong attempt 1, elemental analysis is unlocked. "
            "After wrong attempt 2, MS is unlocked. "
            "After wrong attempt 3, the 13C NMR becomes simplified. "
            "After wrong attempt 4, the empirical formula is shown. "
            "After wrong attempt 5, the molecular formula is shown."
        ),
    },
}