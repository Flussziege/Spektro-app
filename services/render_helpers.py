from __future__ import annotations
import streamlit as st


def init_session_state():
    defaults = {
        "mode": "home",
        "quiz_smiles": None,
        "quiz_name": None,
        "quiz_submitted": False,
        "quiz_correct": None,
        "daily_done_date": None,
        "daily_submitted": False,
        "daily_correct": None,
        "lookup_smiles": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_quiz_state():
    st.session_state["quiz_smiles"] = None
    st.session_state["quiz_name"] = None
    st.session_state["quiz_submitted"] = False
    st.session_state["quiz_correct"] = None


def reset_daily_state():
    st.session_state["daily_submitted"] = False
    st.session_state["daily_correct"] = None


def go_home():
    st.session_state["mode"] = "home"
