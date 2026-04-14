from __future__ import annotations
import streamlit as st
from datetime import date
from services.plotly_nmr import make_interactive_1h_plot

import re
from math import gcd
from functools import reduce
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

from liste_neu import moleküle
from daily_molekuele import moleküle_daily

import generator
import generator2   
import generator5
import hnmr


from services.quiz_logic import (
    pick_random_molecule,
    pick_daily_molecule,
    is_correct_answer,
)

from services.molecule_utils import (
    build_name_maps,
    build_smiles_to_molecule_map,
    smiles_to_pil,
    molecule_exists,
    get_display_name,
    get_difficulty,
    normalize_smiles,
)
from services.render_helpers import (
    init_session_state,
    go_home,
    start_quiz,
    submit_quiz,
    start_daily,
    submit_daily,
    set_lookup,
)

from services.plotly_spectra import (
    make_interactive_13c_plot,
    make_interactive_ir_plot
)

from services.texts import get_text

st.set_page_config(
    page_title= "Spectra Quiz",
    page_icon="🧪",
    layout="wide",
)


def get_light_css() -> str:
    return """
    <style>
    .main {
        background-color: #FFFFFF;
    }

    .stApp {
        background-color: #FFFFFF;
        color: #111827;
    }

    .stButton > button {
        background: #F8FAFC;
        color: #111827;
        border: 1px solid #E5E7EB;
        border-radius: 10px;
        box-shadow: none;
    }

    .stButton > button:hover {
        background: #F1F5F9;
        border-color: #CBD5E1;
    }

    .stButton > button[kind="primary"] {
        background: #111827;
        color: white;
        border: 1px solid #111827;
    }

    .stTextInput input,
    .stSelectbox div[data-baseweb="select"] > div {
        background: #F8FAFC;
        border: 1px solid #E5E7EB;
        border-radius: 10px;
        color: #111827;
    }

    details {
        background: #F8FAFC;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
    }

    .stTabs [data-baseweb="tab"] {
        background: #FFFFFF;
        border: none;
        color: #111827;
    }

    .stTabs [aria-selected="true"] {
        background: #FFFFFF;
    }

    [data-testid="stAlert"] {
        background: #F8FAFC;
        border: 1px solid #E5E7EB;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 95rem;
    }
    </style>
    """


def get_dark_css() -> str:
    return """
    <style>
    .main {
        background-color: #0F172A;
    }

    .stApp {
        background-color: #0F172A;
        color: #E5E7EB;
    }

    /* Oberer Header-Balken */
    header[data-testid="stHeader"] {
        background: #0F172A !important;
    }

    /* Toolbar / obere Leiste */
    [data-testid="stToolbar"] {
        background: #0F172A !important;
    }

    /* Hauptcontainer */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 95rem;
    }

    /* Text */
    .stMarkdown, .stText, p, label, span, h1, h2, h3, h4, h5, h6 {
        color: #E5E7EB;
    }

    /* Buttons */
    .stButton > button {
        background: #1E293B !important;
        color: #E5E7EB !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
        box-shadow: none !important;
    }

    .stButton > button:hover {
        background: #273449 !important;
        border-color: #475569 !important;
    }

    .stButton > button[kind="primary"] {
        background: #E5E7EB !important;
        color: #0F172A !important;
        border: 1px solid #E5E7EB !important;
    }

    /* Inputs */
    .stTextInput input,
    .stNumberInput input,
    .stTextArea textarea {
        background: #1E293B !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
        color: #E5E7EB !important;
    }

    /* Selectbox / Dropdown / Antwortfeld */
    .stSelectbox div[data-baseweb="select"] > div,
    div[data-baseweb="select"] > div {
        background: #1E293B !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
        color: #E5E7EB !important;
    }

    div[data-baseweb="select"] input {
        color: #E5E7EB !important;
    }

    /* Dropdown-Menü selbst */
    div[role="listbox"] {
        background: #1E293B !important;
        color: #E5E7EB !important;
        border: 1px solid #334155 !important;
    }

    div[role="option"] {
        background: #1E293B !important;
        color: #E5E7EB !important;
    }

    div[role="option"]:hover {
        background: #273449 !important;
    }

    /* Segmented control / Button group */
    [data-testid="stBaseButton-segmented_control"] {
        background: #1E293B !important;
        color: #E5E7EB !important;
        border: 1px solid #334155 !important;
    }

    div[role="radiogroup"] {
        background: transparent !important;
    }

    div[role="radiogroup"] > label {
        background: #1E293B !important;
        color: #E5E7EB !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
    }

    div[role="radiogroup"] > label[data-checked="true"] {
        background: #334155 !important;
        color: #FFFFFF !important;
    }

    /* Expander */
    details {
        background: #1E293B !important;
        border: 1px solid #334155 !important;
        border-radius: 12px !important;
    }

    summary {
        color: #E5E7EB !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.25rem;
    }

    .stTabs [data-baseweb="tab"] {
        background: #0F172A !important;
        border: none !important;
        color: #E5E7EB !important;
        border-radius: 8px !important;
    }

    .stTabs [aria-selected="true"] {
        background: #1E293B !important;
        color: #FFFFFF !important;
    }

    /* Alerts */
    [data-testid="stAlert"] {
        background: #1E293B !important;
        border: 1px solid #334155 !important;
        color: #E5E7EB !important;
    }

    /* Plotly-Container */
    .js-plotly-plot, .plotly, .plot-container {
        background: transparent !important;
    }

    /* Tabellen / Codeboxen / sonstige Container */
    [data-testid="stVerticalBlock"] {
        color: #E5E7EB;
    }
    /* Selectbox / Combobox komplett dunkel */
    div[data-baseweb="select"] {
        color: #E5E7EB !important;
    }

    div[data-baseweb="select"] > div {
        background: #1E293B !important;
        border: 1px solid #334155 !important;
        color: #E5E7EB !important;
    }

    div[data-baseweb="select"] span {
        color: #E5E7EB !important;
    }

    div[data-baseweb="select"] input {
        color: #E5E7EB !important;
        -webkit-text-fill-color: #E5E7EB !important;
    }

    /* Das eigentliche Antwortfeld / placeholder */
    [data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        background: #1E293B !important;
        border: 1px solid #334155 !important;
        color: #E5E7EB !important;
    }

    /* Dropdown-Liste im Portal */
    div[role="listbox"] {
        background: #1E293B !important;
        border: 1px solid #334155 !important;
        color: #E5E7EB !important;
    }

    div[role="option"] {
        background: #1E293B !important;
        color: #E5E7EB !important;
    }

    div[role="option"][aria-selected="true"] {
        background: #334155 !important;
        color: #FFFFFF !important;
    }

    div[role="option"]:hover {
        background: #273449 !important;
        color: #FFFFFF !important;
    }
    </style>
    """

init_session_state()

theme_mode = st.session_state.get("theme_mode", "light")

if theme_mode == "dark":
    st.markdown(get_dark_css(), unsafe_allow_html=True)
else:
    st.markdown(get_light_css(), unsafe_allow_html=True)

if "lang_select" not in st.session_state:
    st.session_state["lang_select"] = st.session_state.get("lang", "de")

if "lang" not in st.session_state:
    st.session_state["lang"] = "de"

lang = st.session_state.get("lang_select", st.session_state.get("lang", "de"))

namen_liste, name_to_smiles, smiles_to_name = build_name_maps(moleküle, lang=lang)
daily_names, daily_name_to_smiles, daily_smiles_to_name = build_name_maps(moleküle_daily, lang=lang)

smiles_to_molecule = build_smiles_to_molecule_map(moleküle)
daily_smiles_to_molecule = build_smiles_to_molecule_map(moleküle_daily)    

def render_top_controls():
    col_spacer, col_lang, col_theme = st.columns([6, 1, 1])

    with col_lang:
        lang = st.segmented_control(
            t("language_label"),
            options=["de", "en"],
            format_func=lambda x: "🇩🇪 DE" if x == "de" else "🇬🇧 EN",
            key="lang_select",
            selection_mode="single",
            width="content",
        )
        if lang is not None:
            st.session_state["lang"] = lang

    with col_theme:
        st.segmented_control(
            t("theme_label"),
            options=["light", "dark"],
            format_func=lambda x: "☀️" if x == "light" else "🌙",
            key="theme_mode",
            selection_mode="single",
            width="content",
        )

def t(key: str, **kwargs) -> str:
    lang = st.session_state.get("lang_select", st.session_state.get("lang", "de"))
    return get_text(lang, key, **kwargs)

def difficulty_text(level: str) -> str:
    return t(f"difficulty_{level}")

def get_molecule_data(smiles: str, daily: bool = False) -> tuple[dict | None, str, str]:
    smiles_norm = normalize_smiles(smiles)
    current_lang = st.session_state.get("lang_select", st.session_state.get("lang", "de"))

    if daily:
        mol = daily_smiles_to_molecule.get(smiles_norm)
    else:
        mol = smiles_to_molecule.get(smiles_norm)

    if not mol:
        fallback_name = "Unknown" if current_lang == "en" else "Unbekannt"
        return None, fallback_name, "medium"

    return mol, get_display_name(mol, lang=current_lang), get_difficulty(mol)

def get_molecular_formula(smiles: str) -> str | None:
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    return rdMolDescriptors.CalcMolFormula(mol)


def get_empirical_formula_from_molecular(formula: str) -> str:
    parts = re.findall(r"([A-Z][a-z]*)(\d*)", formula)
    if not parts:
        return formula

    parsed = []
    counts = []

    for element, count_str in parts:
        count = int(count_str) if count_str else 1
        parsed.append((element, count))
        counts.append(count)

    divisor = reduce(gcd, counts)
    if divisor <= 1:
        return formula

    result = ""
    for element, count in parsed:
        reduced = count // divisor
        result += element if reduced == 1 else f"{element}{reduced}"
    return result


def get_empirical_formula_hint(smiles: str) -> str | None:
    molecular = get_molecular_formula(smiles)
    if not molecular:
        return None

    empirical = get_empirical_formula_from_molecular(molecular)
    if empirical == molecular:
        return empirical
    return f"({empirical})n"

def formula_to_html_subscripts(formula: str) -> str:
    """
    Macht aus C8H10 -> C<sub>8</sub>H<sub>10</sub>
    """
    return re.sub(r"(\d+)", r"<sub>\1</sub>", formula)


def empirical_formula_with_n(smiles: str) -> str | None:
    """
    Gibt die empirische Formel im Stil C2n H6n zurück.
    Beispiel:
    - Summenformel C4H12O2
    - empirische Formel CH3O
    - Ausgabe: Cn H3n On
    bzw. bei Teilern >1: C2n H6n
    """
    molecular = get_molecular_formula(smiles)
    if not molecular:
        return None

    parts = re.findall(r"([A-Z][a-z]*)(\d*)", molecular)
    if not parts:
        return None

    parsed = []
    counts = []

    for element, count_str in parts:
        count = int(count_str) if count_str else 1
        parsed.append((element, count))
        counts.append(count)

    divisor = reduce(gcd, counts)
    if divisor <= 1:
        return molecular

    chunks = []
    for element, count in parsed:
        reduced = count // divisor

        if reduced == 1:
            chunks.append(f"{element}n")
        else:
            chunks.append(f"{element}{reduced}n")

    return " ".join(chunks)


def get_daily_unlock_message(attempts: int) -> str | None:
    if attempts == 1:
        return t("daily_new_hint_ea")
    if attempts == 2:
        return t("daily_new_hint_ms")
    if attempts == 3:
        return t("daily_new_hint_c13_easy")
    if attempts == 4:
        return t("daily_new_hint_empirical")
    if attempts == 5:
        return t("daily_new_hint_formula")
    return None

def empirical_formula_with_n_html(smiles: str) -> str | None:
    molecular = get_molecular_formula(smiles)
    if not molecular:
        return None

    parts = re.findall(r"([A-Z][a-z]*)(\d*)", molecular)
    if not parts:
        return None

    parsed = []
    counts = []

    for element, count_str in parts:
        count = int(count_str) if count_str else 1
        parsed.append((element, count))
        counts.append(count)

    divisor = reduce(gcd, counts)
    if divisor <= 1:
        return formula_to_html_subscripts(molecular)

    chunks = []
    for element, count in parsed:
        reduced = count // divisor

        if reduced == 1:
            chunks.append(f"{element}<sub>n</sub>")
        else:
            chunks.append(f"{element}<sub>{reduced}n</sub>")

    return " ".join(chunks)

def card(title: str, text: str):
    theme_mode = st.session_state.get("theme_mode", "light")

    if theme_mode == "dark":
        bg = "#1E293B"
        border = "#334155"
        text_color = "#CBD5E1"
        title_color = "#E5E7EB"
    else:
        bg = "#F8FAFC"
        border = "#E5E7EB"
        text_color = "#475569"
        title_color = "#111827"

    st.html(f"""
    <div style="
        background:{bg};
        border:1px solid {border};
        border-radius:16px;
        padding:1.2rem;
        box-shadow:0 1px 3px rgba(15,23,42,0.03);
    ">
        <div style="font-size:1.1rem;font-weight:600;color:{title_color};">
            {title}
        </div>
        <div style="color:{text_color};">
            {text}
        </div>
    </div>
    """)


def render_spectra_tabs(
    smiles: str,
    show_structure: bool = False,
    show_c13: bool = True,
    show_h1: bool = True,
    show_ir: bool = True,
    show_ea: bool = True,
    show_ms: bool = False,
    c13_easy_mode: bool = False,
):
    tabs = []
    tab_keys = []

    theme_mode = st.session_state.get("theme_mode", "light")

    if show_c13:
        tabs.append(t("c13_nmr_title"))
        tab_keys.append("c13")
    if show_h1:
        tabs.append(t("h1_nmr_title"))
        tab_keys.append("h1")
    if show_ir:
        tabs.append(t("ir_title"))
        tab_keys.append("ir")
    if show_ea:
        tabs.append(t("ea_title"))
        tab_keys.append("ea")
    if show_ms:
        tabs.append(t("ms_title"))
        tab_keys.append("ms")
    if show_structure:
        tabs.append(t("structure_title"))
        tab_keys.append("structure")

    rendered_tabs = st.tabs(tabs)

    for tab, key in zip(rendered_tabs, tab_keys):
        with tab:
            if key == "c13":
                st.subheader(t("c13_nmr_title"))
                try:
                    c13_result = generator.simulate_13c_nmr(
                        smiles,
                        seed=42,
                        plot=False,
                        show_title=show_structure,
                        easymode=c13_easy_mode,
                        width=0.035,
                        testrun=True,
                    )

                    fig1 = make_interactive_13c_plot(
                         c13_result,
                        smiles,
                        show_integrals=show_structure,
                        theme_mode=theme_mode,
                        )

                    st.plotly_chart(
                        fig1,
                        width="stretch",
                        config={
                            "scrollZoom": True,
                            "displaylogo": False,
                            "doubleClick": "reset",
                            "modeBarButtonsToRemove": [
                                "zoom2d",
                                "select2d",
                                "lasso2d",
                                "zoomIn2d",
                                "zoomOut2d",
                                "autoScale2d",
                            ],
                        },
                        theme=None,
                    )
                except Exception as e:
                    st.error(f"13C NMR: {e}")

            elif key == "h1":
                st.subheader(t("h1_nmr_title"))
                try:
                    nmr_result = hnmr.simulate_1h_nmr(
                        smiles,
                        seed=42,
                        plot=False,
                        verbose=False,
                        line_width=0.008,
                        show_integrals=show_structure,
                        show_title=show_structure,
                        testrun=True,
                    )

                    fig2 = make_interactive_1h_plot(
                        nmr_result=nmr_result,
                        smiles=smiles,
                        show_integrals=show_structure,
                        theme_mode=theme_mode,
                    )

                    st.plotly_chart(
                        fig2,
                        width="stretch",
                        config={
                            "scrollZoom": True,
                            "displaylogo": False,
                            "doubleClick": "reset",
                            "modeBarButtonsToRemove": [
                                "zoom2d",
                                "select2d",
                                "lasso2d",
                                "zoomIn2d",
                                "zoomOut2d",
                                "autoScale2d",
                            ],
                        },
                        theme=None,
                    )

                except Exception as e:
                    st.error(f"1H NMR: {e}")

            elif key == "ir":
                st.subheader(t("ir_title"))
                try:
                    ir_result = generator2.simulate_ir(
                        smiles,
                        seed=42,
                        plot=False,
                        show_title=True,
                        testrun=True,
                    )

                    fig3 = make_interactive_ir_plot(
                        ir_result,
                        smiles,
                        show_integrals=show_structure,
                        theme_mode=theme_mode,
                    )

                    st.plotly_chart(
                        fig3,
                        width="stretch",
                        config={
                            "scrollZoom": True,
                            "displaylogo": False,
                            "doubleClick": "reset",
                            "modeBarButtonsToRemove": [
                                "zoom2d",
                                "select2d",
                                "lasso2d",
                                "zoomIn2d",
                                "zoomOut2d",
                                "autoScale2d",
                            ],
                        },
                        theme=None,
                    )
                except Exception as e:
                    st.error(f"IR: {e}")

            elif key == "ea":
                st.subheader(t("ea_title"))
                try:
                    result = generator5.elementaranalyse(smiles)
                    if result:
                        for el, perc in sorted(result.items()):
                            st.write(f"**{el}**: {perc:.2f} %")
                    else:
                        st.warning(t("ea_missing"))
                except Exception as e:
                    st.error(t("ea_error", error=e))

            elif key == "ms":
                st.subheader(t("ms_title"))
                st.info(t("ms_placeholder"))

            elif key == "structure":
                st.subheader(t("structure_title"))
                try:
                    img = smiles_to_pil(smiles)
                    if img is not None:
                        st.image(img, width=320)
                    else:
                        st.warning(t("structure_missing"))
                except Exception as e:
                    st.error(t("structure_error", error=e))


def render_home():
    render_top_controls()
    st.title(t("home_title"))
    st.write(t("home_subtitle"))

    col1, col2 = st.columns(2)

    with col2:
        card(t("card_quiz_title"), t("card_quiz_text"))
        if st.button(t("quiz_start"), width="stretch"):
            mol = pick_random_molecule(moleküle)
            start_quiz(mol)
            st.rerun()

    with col1:
        card(t("card_daily_title"), t("card_daily_text"))
        if st.button(t("daily_open"), width="stretch"):
            mol = pick_daily_molecule(moleküle_daily)
            start_daily(mol)
            st.rerun()

    with st.expander(t("lookup_expander"), expanded=False):
        selected_name = st.selectbox(t("lookup_name"), [""] + namen_liste)
        smiles_input = st.text_input(t("lookup_smiles"))

        if st.button(t("lookup_submit"), width="stretch"):
            chosen_smiles = None

            if selected_name:
                chosen_smiles = name_to_smiles.get(selected_name.lower())
            elif smiles_input.strip():
                if molecule_exists(smiles_input.strip()):
                    chosen_smiles = normalize_smiles(smiles_input)
                else:
                    st.error(t("invalid_smiles"))
                    return
            else:
                st.warning(t("lookup_missing_input"))
                return

            set_lookup(chosen_smiles)
            st.rerun()

    st.markdown("---")
    st.info(t("disclaimer"))


def render_quiz_help():
    with st.expander(t("how_to_play"), expanded=False):
        st.markdown(f"**{t('how_to_play_quiz_title')}**")

        st.markdown(f"**{t('help_1h_title')}**")
        st.write(t("help_1h_quiz_text"))

        st.markdown(f"**{t('help_navigation_title')}**")
        st.write(t("help_navigation_text"))

        st.markdown(f"**{t('help_ea_title')}**")
        st.write(t("help_ea_text"))

        st.markdown(f"**{t('help_quiz_attempts_title')}**")
        st.write(t("help_quiz_attempts_text"))

        st.markdown(f"**{t('help_simulation_title')}**")
        st.write(t("help_simulation_text"))

def render_quiz():
    smiles = st.session_state.get("quiz_smiles")

    if not smiles:
        st.warning(t("no_quiz_active"))
        if st.button(t("back_home")):
            go_home()
            st.rerun()
        return

    mol_data, correct_name, difficulty = get_molecule_data(smiles, daily=False)

    st.title(t("quiz_title"))
    st.caption(f"{t('difficulty_label')}: {difficulty_text(difficulty)}")

    render_quiz_help()
    render_top_controls()

    if st.session_state["quiz_submitted"]:
        st.markdown("---")

        user_answer = st.session_state.get("quiz_user_answer", "")
        user_smiles = st.session_state.get("quiz_user_smiles")
        user_name = user_answer if user_answer else t("no_selection")

        if st.session_state["quiz_correct"]:
            st.success(t("correct_quiz", name=correct_name))

            col_left, col_center, col_right = st.columns([1, 2, 1])

            with col_center:
                try:
                    img = smiles_to_pil(smiles)
                    if img is not None:
                        st.image(img, caption=correct_name, width="stretch")
                except Exception as e:
                    st.warning(t("structure_display_error", error=e))

        else:
            st.error(t("wrong_quiz", name=correct_name))


            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f"### {t('correct_label', name=correct_name)}")
                try:
                    img_correct = smiles_to_pil(smiles)
                    if img_correct is not None:
                        st.image(img_correct, width=320)
                except Exception as e:
                    st.warning(t("structure_display_error", error=e))

            with col2:
                st.markdown(f"### {t('your_answer_label', name=user_name)}")
                if user_smiles:
                    try:
                        img_user = smiles_to_pil(user_smiles)
                        if img_user is not None:
                            st.image(img_user, width=320)
                    except Exception as e:
                        st.warning(t("structure_display_error", error=e))
                else:
                    st.info(t("no_answer_image"))

        col_a, col_b = st.columns(2)

        with col_a:
            if st.button(t("another_quiz"), width="stretch"):
                mol = pick_random_molecule(moleküle)
                start_quiz(mol)
                st.rerun()

        with col_b:
            if st.button(t("startpage"), width="stretch", key="quiz_home_end"):
                go_home()
                st.rerun()

        return

    render_spectra_tabs(smiles, show_structure=False)

    answer = st.selectbox(
        t("quiz_question"),
        [""] + namen_liste,
        key="quiz_answer_select",
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button(t("quiz_submit"), type="primary", width="stretch"):
            selected_smiles = name_to_smiles.get(answer.strip().lower()) if answer else None
            correct = is_correct_answer(answer, smiles, name_to_smiles)

            st.session_state["quiz_user_answer"] = answer
            st.session_state["quiz_user_smiles"] = selected_smiles

            submit_quiz(correct)
            st.rerun()

    with col2:
        if st.button(t("back_home"), width="stretch"):
            go_home()
            st.rerun()

def render_daily_help():
    with st.expander(t("how_to_play"), expanded=False):
        st.markdown(f"**{t('how_to_play_daily_title')}**")

        st.markdown(f"**{t('help_1h_title')}**")
        st.write(t("help_1h_quiz_text"))

        st.markdown("**13C NMR**")
        st.write(t("help_13c_daily_text"))

        st.markdown(f"**{t('help_navigation_title')}**")
        st.write(t("help_navigation_text"))

        st.markdown(f"**{t('help_ea_title')}**")
        st.write(t("help_ea_text"))

        st.markdown(f"**{t('help_daily_attempts_title')}**")
        st.write(t("help_daily_attempts_text"))

        st.markdown(f"**{t('help_daily_hints_title')}**")
        st.write(t("help_daily_hints_text"))

        st.markdown(f"**{t('help_simulation_title')}**")
        st.write(t("help_simulation_text"))

def render_daily():
    smiles = st.session_state.get("daily_smiles")
    today = date.today().isoformat()

    # Safety net für ältere Sessions
    if "daily_attempt_count" not in st.session_state:
        st.session_state["daily_attempt_count"] = 0
    if "daily_wrong_guesses" not in st.session_state:
        st.session_state["daily_wrong_guesses"] = []
    if "daily_last_feedback" not in st.session_state:
        st.session_state["daily_last_feedback"] = None
    if "daily_user_smiles" not in st.session_state:
        st.session_state["daily_user_smiles"] = None

    st.title(t("daily_title"))


    if (
        st.session_state["daily_done_date"] == today
        and not st.session_state["daily_submitted"]
    ):
        st.success(t("daily_done"))
        if st.button(t("back_home"), key="daily_done_home", width="stretch"):
            go_home()
            st.rerun()
        return

    if not smiles:
        mol = pick_daily_molecule(moleküle_daily)
        start_daily(mol)
        smiles = st.session_state.get("daily_smiles")

        if not smiles:
            st.warning(t("no_quiz_active"))
            if st.button(t("back_home"), key="daily_home_fallback", width="stretch"):
                go_home()
                st.rerun()
            return

    _, correct_name, difficulty = get_molecule_data(smiles, daily=True)

    attempts = st.session_state.get("daily_attempt_count", 0)
    wrong_guesses = st.session_state.get("daily_wrong_guesses", [])

    show_ea = attempts >= 1
    show_ms = attempts >= 2
    c13_easy_mode = attempts >= 3
    show_empirical_formula = attempts >= 4
    show_molecular_formula = attempts >= 5

    st.markdown("<div id='top-anchor'></div>", unsafe_allow_html=True)

    st.write("")
    st.caption(f"{t('difficulty_label')}: {difficulty_text(difficulty)}")
    st.caption(t("daily_attempts_label", count=attempts))

    render_daily_help()
    render_top_controls()

    unlock_message = st.session_state.get("daily_last_feedback")
    if unlock_message:
        st.info(unlock_message)
        st.session_state["daily_last_feedback"] = None

    if st.session_state["daily_submitted"] and st.session_state["daily_correct"]:
        st.success(t("correct_daily", name=correct_name))

        st.markdown(f"### {t('wrong_guesses_title')}")
        if wrong_guesses:
            for guess in wrong_guesses:
                st.write(f"- {guess}")
        else:
            st.write(t("no_selection"))

        if st.button(t("startpage"), key="daily_home_bottom", width="stretch"):
            st.session_state["daily_submitted"] = False
            go_home()
            st.rerun()
        return

    render_spectra_tabs(
        smiles,
        show_structure=False,
        show_c13=True,
        show_h1=True,
        show_ir=True,
        show_ea=show_ea,
        show_ms=show_ms,
        c13_easy_mode=c13_easy_mode,
    )

    if show_empirical_formula:
        empirical_n_html = empirical_formula_with_n_html(smiles)
        if empirical_n_html:
            st.markdown(
                f"**{t('empirical_formula_n_label_plain')}** {empirical_n_html}",
                unsafe_allow_html=True,
            )

    if show_molecular_formula:
        molecular_formula = get_molecular_formula(smiles)
        if molecular_formula:
            formula_html = formula_to_html_subscripts(molecular_formula)
            st.markdown(
                f"**{t('molecular_formula_label_plain')}** {formula_html}",
                unsafe_allow_html=True,
            )

    if st.session_state["daily_submitted"] and st.session_state["daily_correct"] is False:
        st.error(t("daily_try_again"))
        st.session_state["daily_submitted"] = False

    st.markdown(f"### {t('wrong_guesses_title')}")
    if wrong_guesses:
        for guess in wrong_guesses:
            st.write(f"- {guess}")
    else:
        st.write(t("no_selection"))

    excluded = set(wrong_guesses)
    available_daily_names = [""] + [name for name in daily_names if name not in excluded]

    current_daily_value = st.session_state.get("daily_answer_select", "")
    if current_daily_value not in available_daily_names:
        st.session_state["daily_reset_selection"] = True

    if "daily_reset_selection" not in st.session_state:
        st.session_state["daily_reset_selection"] = False

    if st.session_state.get("daily_reset_selection"):
        st.session_state["daily_answer_select"] = ""
        st.session_state["daily_reset_selection"] = False

    answer = st.selectbox(
        t("daily_question"),
        available_daily_names,
        key="daily_answer_select",
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button(t("daily_submit"), type="primary", width="stretch"):
            cleaned_answer = answer.strip() if answer else ""

            if not cleaned_answer:
                st.warning(t("daily_invalid_selection"))
                return

            if cleaned_answer in wrong_guesses:
                st.warning(t("daily_already_guessed"))
                return

            if cleaned_answer not in daily_names:
                st.warning(t("daily_invalid_selection"))
                return

            selected_smiles = daily_name_to_smiles.get(cleaned_answer.lower())
            correct = is_correct_answer(cleaned_answer, smiles, daily_name_to_smiles)

            st.session_state["daily_user_answer"] = cleaned_answer
            st.session_state["daily_user_smiles"] = selected_smiles
            st.session_state["daily_submitted"] = True
            st.session_state["daily_correct"] = correct

            if correct:
                st.session_state["daily_done_date"] = date.today().isoformat()
            else:
                st.session_state["daily_attempt_count"] += 1
                if cleaned_answer not in st.session_state["daily_wrong_guesses"]:
                    st.session_state["daily_wrong_guesses"].append(cleaned_answer)

                attempts_now = st.session_state["daily_attempt_count"]
                st.session_state["daily_last_feedback"] = get_daily_unlock_message(attempts_now)

                st.session_state["daily_reset_selection"] = True

            st.rerun()

    with col2:
        if st.button(t("back_home"), key="daily_home_top", width="stretch"):
            go_home()
            st.rerun()


def render_lookup():
    smiles = st.session_state["lookup_smiles"]


    st.title(t("lookup_title"))
    render_top_controls()

    if not smiles:
        st.warning(t("lookup_empty"))
        if st.button(t("back_home"), key="lookup_home_empty"):
            go_home()
            st.rerun()
        return

    mol_data, display_name, difficulty = get_molecule_data(smiles, daily=False)

    if mol_data:
        st.subheader(display_name)
        st.caption(f"{t('difficulty_label')}: {difficulty_text(difficulty)}")

    st.write(f"**SMILES:** `{smiles}`")
    render_spectra_tabs(smiles, show_structure=True)

    if st.button(t("back_home"), key="lookup_home", width="stretch"):
        go_home()
        st.rerun()

mode = st.session_state["mode"]

if mode == "home":
    render_home()
elif mode == "quiz":
    render_quiz()
elif mode == "daily":
    render_daily()
elif mode == "lookup":
    render_lookup()
else:
    go_home()
    render_home()
