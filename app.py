from __future__ import annotations
import streamlit as st
from datetime import date
from services.plotly_nmr import make_interactive_1h_plot

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

st.html("""
<style>

/* Hintergrund der gesamten App minimal wärmer */
.main {
    background-color: #FFFFFF;
}

/* Buttons leicht grau */
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

/* Primäre Buttons (z.B. Quiz starten) */
.stButton > button[kind="primary"] {
    background: #111827;
    color: white;
    border: 1px solid #111827;
}

/* Input-Felder (SMILES / Selectbox) */
.stTextInput input,
.stSelectbox div[data-baseweb="select"] > div {
    background: #F8FAFC;
    border: 1px solid #E5E7EB;
    border-radius: 10px;
}

/* Expander (Lookup) */
details {
    background: #F8FAFC;
    border: 1px solid #E5E7EB;
    border-radius: 12px;
}

/* Tabs nur leicht anpassen, nicht überschreiben */
.stTabs [data-baseweb="tab"] {
    background: #FFFFFF;
    border: none;
}

.stTabs [aria-selected="true"] {
    background: #FFFFFF;
}

/* Alerts (Ergebnisboxen) */
[data-testid="stAlert"] {
    background: #F8FAFC;
    border: 1px solid #E5E7EB;
}

/* Allgemeine Container etwas luftiger */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 95rem;
}

</style>
""")

init_session_state()

if "lang_select" not in st.session_state:
    st.session_state["lang_select"] = st.session_state.get("lang", "de")

if "lang" not in st.session_state:
    st.session_state["lang"] = "de"

lang = st.session_state.get("lang_select", st.session_state.get("lang", "de"))

namen_liste, name_to_smiles, smiles_to_name = build_name_maps(moleküle, lang=lang)
daily_names, daily_name_to_smiles, daily_smiles_to_name = build_name_maps(moleküle_daily, lang=lang)

smiles_to_molecule = build_smiles_to_molecule_map(moleküle)
daily_smiles_to_molecule = build_smiles_to_molecule_map(moleküle_daily)                                                                       

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

def card(title: str, text: str):
    st.html(f"""
    <div style="
        background:#F8FAFC;
        border:1px solid #E5E7EB;
        border-radius:16px;
        padding:1.2rem;
        box-shadow:0 1px 3px rgba(15,23,42,0.03);
    ">
        <div style="font-size:1.1rem;font-weight:600;">
            {title}
        </div>
        <div style="color:#475569;">
            {text}
        </div>
    </div>
    """)


def render_spectra_tabs(smiles: str, show_structure: bool = False):

    if show_structure:
        tab1, tab2, tab3, tab4, tab5 = st.tabs([t("c13_nmr_title"), t("h1_nmr_title"), t("ir_title"), t("ea_title"), t("structure_title")])
    else: 
        tab1, tab2, tab3, tab4 = st.tabs([t("c13_nmr_title"), t("h1_nmr_title"), t("ir_title"), t("ea_title")])

    with tab1:
        st.subheader(t("c13_nmr_title"))
        try:
            c13_result = generator.simulate_13c_nmr(
                smiles,
                seed=42,
                plot=False,
                show_title=show_structure,
                easymode=False,
                width=0.035,
                testrun=True,
            )

            fig1 = make_interactive_13c_plot(c13_result, smiles, show_integrals=show_structure)

            st.plotly_chart(
                fig1,
                use_container_width=True,
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

    with tab2:
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
            )
    
            st.plotly_chart(
                fig2,
                use_container_width=True,
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

    with tab3:
        st.subheader(t("ir_title"))
        try:
            ir_result = generator2.simulate_ir(
                smiles,
                seed=42,
                plot=False,
                show_title=True,
                testrun=True,
            )

            fig3 = make_interactive_ir_plot(ir_result, smiles, show_integrals=show_structure)

            st.plotly_chart(
                fig3,
                use_container_width=True,
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

    with tab4:
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

    if show_structure:
        with tab5:
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
    col_title, col_lang = st.columns([5, 1])

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

    with col_title:
        st.title(t("home_title"))

    st.write(t("home_subtitle"))

    col1, col2 = st.columns(2)

    with col2:
        card(t("card_quiz_title"), t("card_quiz_text"))
        if st.button(t("quiz_start"), use_container_width=True):
            mol = pick_random_molecule(moleküle)
            start_quiz(mol)
            st.rerun()

    with col1:
        card(t("card_daily_title"), t("card_daily_text"))
        if st.button(t("daily_open"), use_container_width=True):
            mol = pick_daily_molecule(moleküle_daily)
            start_daily(mol)
            st.rerun()

    with st.expander(t("lookup_expander"), expanded=False):
        selected_name = st.selectbox(t("lookup_name"), [""] + namen_liste)
        smiles_input = st.text_input(t("lookup_smiles"))

        if st.button(t("lookup_submit"), use_container_width=True):
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
                        st.image(img, caption=correct_name, use_container_width=True)
                except Exception as e:
                    st.warning(t("structure_display_error", error=e))

        else:
            st.error(t("wrong_quiz", name=correct_name))
            print(user_smiles)

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
            if st.button(t("another_quiz"), use_container_width=True):
                mol = pick_random_molecule(moleküle)
                start_quiz(mol)
                st.rerun()

        with col_b:
            if st.button(t("startpage"), use_container_width=True, key="quiz_home_end"):
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
        if st.button(t("quiz_submit"), type="primary", use_container_width=True):
            selected_smiles = name_to_smiles.get(answer.strip().lower()) if answer else None
            correct = is_correct_answer(answer, smiles, name_to_smiles)

            st.session_state["quiz_user_answer"] = answer
            st.session_state["quiz_user_smiles"] = selected_smiles

            submit_quiz(correct)
            st.rerun()

    with col2:
        if st.button(t("back_home"), use_container_width=True):
            go_home()
            st.rerun()

def render_daily():
    smiles = st.session_state.get("daily_smiles")
    today = date.today().isoformat()

    st.title(t("daily_title"))

    if (
        st.session_state["daily_done_date"] == today
        and not st.session_state["daily_submitted"]
    ):
        st.success(t("daily_done"))
        if st.button(t("back_home"), key="daily_done_home"):
            go_home()
            st.rerun()
        return

    if not smiles:
        mol = pick_daily_molecule(moleküle_daily)
        start_daily(mol)
        smiles = st.session_state.get("daily_smiles")

        if not smiles:
            st.warning(t("no_quiz_active"))
            if st.button(t("back_home"), key="daily_home_fallback"):
                go_home()
                st.rerun()
            return

    mol_data, correct_name, difficulty = get_molecule_data(smiles, daily=True)

    st.caption(f"{t('difficulty_label')}: {difficulty_text(difficulty)}")

    if st.session_state["daily_submitted"]:
        st.markdown("---")

        user_answer = st.session_state.get("daily_user_answer", "")
        user_smiles = st.session_state.get("daily_user_smiles")
        user_name = user_answer if user_answer else t("no_selection")

        if st.session_state["daily_correct"]:
            st.success(t("correct_daily", name=correct_name))

            col_left, col_center, col_right = st.columns([1, 2, 1])

            with col_center:
                try:
                    img = smiles_to_pil(smiles)
                    if img is not None:
                        st.image(img, caption=correct_name, use_container_width=True)
                except Exception as e:
                    st.warning(t("structure_display_error", error=e))

        else:
            st.error(t("wrong_daily", name=correct_name))

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

        if st.button(t("startpage"), key="daily_home_bottom", use_container_width=True):
            st.session_state["daily_submitted"] = False
            go_home()
            st.rerun()

        return

    render_spectra_tabs(smiles, show_structure=False)

    answer = st.selectbox(
        t("daily_question"),
        [""] + daily_names,
        key="daily_answer_select",
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button(t("daily_submit"), type="primary", use_container_width=True):
            selected_smiles = daily_name_to_smiles.get(answer.strip().lower()) if answer else None
            correct = is_correct_answer(answer, smiles, daily_name_to_smiles)

            st.session_state["daily_user_answer"] = answer
            st.session_state["daily_user_smiles"] = selected_smiles

            submit_daily(correct)
            st.rerun()

    with col2:
        if st.button(t("back_home"), key="daily_home_top", use_container_width=True):
            go_home()
            st.rerun()

def render_lookup():
    smiles = st.session_state["lookup_smiles"]

    st.title(t("lookup_title"))

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

    if st.button(t("back_home"), key="lookup_home", use_container_width=True):
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
