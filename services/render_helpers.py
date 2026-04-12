from __future__ import annotations
import streamlit as st
from datetime import date


def init_session_state():
    defaults = {
        "mode": "home",

        "quiz_smiles": None,
        "quiz_name": None,
        "quiz_submitted": False,
        "quiz_correct": None,

        "daily_smiles": None,
        "daily_name": None,
        "daily_submitted": False,
        "daily_correct": None,
        "daily_done_date": None,

        "lookup_smiles": None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def go_home():
    st.session_state["mode"] = "home"


def start_quiz(mol: dict):
    st.session_state["quiz_smiles"] = mol["smiles"]
    st.session_state["quiz_name"] = mol["name"]
    st.session_state["quiz_submitted"] = False
    st.session_state["quiz_correct"] = None
    st.session_state["mode"] = "quiz"


def submit_quiz(correct: bool):
    st.session_state["quiz_submitted"] = True
    st.session_state["quiz_correct"] = correct


def start_daily(mol: dict):
    st.session_state["daily_smiles"] = mol["smiles"]
    st.session_state["daily_name"] = mol["name"]
    st.session_state["daily_submitted"] = False
    st.session_state["daily_correct"] = None
    st.session_state["mode"] = "daily"


def submit_daily(correct: bool):
    st.session_state["daily_submitted"] = True
    st.session_state["daily_correct"] = correct
    st.session_state["daily_done_date"] = date.today().isoformat()


def set_lookup(smiles: str):
    st.session_state["lookup_smiles"] = smiles
    st.session_state["mode"] = "lookup"
