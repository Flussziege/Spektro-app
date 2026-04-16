from __future__ import annotations
import streamlit as st
from datetime import date


def init_session_state():
    defaults = {
        "mode": "home",

        # normales Quiz
        "quiz_smiles": None,
        "quiz_name": None,
        "quiz_submitted": False,
        "quiz_correct": None,
        "quiz_user_answer": "",
        "quiz_user_smiles": None,

        # Daily Quiz
        "daily_smiles": None,
        "daily_name": None,
        "daily_submitted": False,
        "daily_correct": None,
        "daily_done_date": None,
        "daily_user_answer": "",
        "daily_user_smiles": None,
        "daily_attempt_count": 0,
        "daily_wrong_guesses": [],
        "daily_last_feedback": None,
        "daily_reset_selection": False,

        #light/dark design
        "theme": "light",

        # Lookup
        "lookup_smiles": None,

        # Sprache
        "lang": "de",

        #aufgeben und wechsel zu lookup
        "quiz_gave_up": False,  
        "daily_gave_up": False,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value



def go_home():
    st.session_state["mode"] = "home"


def start_quiz(mol: dict):
    st.session_state["quiz_smiles"] = mol["smiles"]
    st.session_state["quiz_name"] = mol.get("name_de", mol.get("name_en", "Unbekannt"))
    st.session_state["quiz_submitted"] = False
    st.session_state["quiz_correct"] = None
    st.session_state["quiz_user_answer"] = ""
    st.session_state["quiz_user_smiles"] = None
    st.session_state["mode"] = "quiz"
    st.session_state["quiz_gave_up"] = False


def submit_quiz(correct: bool):
    st.session_state["quiz_submitted"] = True
    st.session_state["quiz_correct"] = correct


def start_daily(mol: dict):
    st.session_state["daily_smiles"] = mol["smiles"]
    st.session_state["daily_name"] = mol.get("name_de", mol.get("name_en", "Unbekannt"))
    st.session_state["daily_submitted"] = False
    st.session_state["daily_correct"] = None
    st.session_state["daily_user_answer"] = ""
    st.session_state["daily_user_smiles"] = None
    st.session_state["daily_attempt_count"] = 0
    st.session_state["daily_wrong_guesses"] = []
    st.session_state["daily_last_feedback"] = None
    st.session_state["mode"] = "daily"
    st.session_state["daily_reset_selection"] = False
    st.session_state["daily_gave_up"] = False


def submit_daily(correct: bool):
    st.session_state["daily_submitted"] = True
    st.session_state["daily_correct"] = correct
    if correct:
        st.session_state["daily_done_date"] = date.today().isoformat()


def set_lookup(smiles: str):
    st.session_state["lookup_smiles"] = smiles
    st.session_state["mode"] = "lookup"


def give_up_quiz():
    st.session_state["quiz_submitted"] = True
    st.session_state["quiz_correct"] = False
    st.session_state["quiz_gave_up"] = True
    st.session_state["quiz_user_answer"] = ""
    st.session_state["quiz_user_smiles"] = None


def give_up_daily():
    st.session_state["daily_submitted"] = True
    st.session_state["daily_correct"] = False
    st.session_state["daily_gave_up"] = True
    st.session_state["daily_done_date"] = date.today().isoformat()
    st.session_state["daily_user_answer"] = ""
    st.session_state["daily_user_smiles"] = None