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
    smiles_to_pil,
    molecule_exists,
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

st.set_page_config(
    page_title="Spektren Quiz",
    layout="wide",
)

st.html("""
<style>
/* Hauptbereich luftiger */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}

/* Überschriften klar und ruhig */
h1, h2, h3 {
    letter-spacing: -0.02em;
    font-weight: 600;
}

/* Buttons klinisch und ruhig */
.stButton > button {
    background: white;
    color: #111827;
    border: 1px solid #E5E7EB;
    border-radius: 10px;
    box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
}

.stButton > button:hover {
    border-color: #CBD5E1;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.06);
}

/* Primäre Buttons etwas dunkler, aber nicht bunt */
.stButton > button[kind="primary"] {
    background: #111827;
    color: white;
    border: 1px solid #111827;
}

/* Expander sehr sauber */
details {
    border: 1px solid #E5E7EB;
    border-radius: 12px;
    background: #FFFFFF;
}

/* Tabs ruhiger */
.stTabs [data-baseweb="tab-list"] {
    gap: 0.5rem;
}

.stTabs [data-baseweb="tab"] {
    background: #F8FAFC;
    border: 1px solid #E5E7EB;
    border-radius: 10px 10px 0 0;
    padding: 0.5rem 0.9rem;
}

.stTabs [aria-selected="true"] {
    background: #FFFFFF;
    border-bottom-color: #FFFFFF;
}

/* Inputs und Selectboxen klarer */
.stTextInput input, .stSelectbox div[data-baseweb="select"] > div {
    border-radius: 10px;
}

/* Alert-Boxen dezenter */
[data-testid="stAlert"] {
    border-radius: 12px;
    border: 1px solid #E5E7EB;
    box-shadow: none;
}
</style>
""")

init_session_state()

namen_liste, name_to_smiles, smiles_to_name = build_name_maps(moleküle)
daily_names, daily_name_to_smiles, daily_smiles_to_name = build_name_maps(moleküle_daily)

def card(title: str, text: str):
    st.html(f"""
    <div style="
        background:#FFFFFF;
        border:1px solid #E5E7EB;
        border-radius:16px;
        padding:1.2rem;
        box-shadow:0 1px 3px rgba(15,23,42,0.04);
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
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["13C NMR", "1H NMR", "IR", "EA", "Struktur"])
    else: 
        tab1, tab2, tab3, tab4 = st.tabs(["13C NMR", "1H NMR", "IR", "EA"])

    with tab1:
        st.subheader("13C NMR")
        try:
            fig1 = generator.simulate_13c_nmr(
                smiles,
                seed=42,
                plot=False,
                show_title= show_structure,
                easymode=False,
            )
            st.pyplot(fig1, clear_figure=True)
        except Exception as e:
            st.error(f"13C NMR konnte nicht erzeugt werden: {e}")

    with tab2:
        st.subheader("1H NMR")
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
            st.error(f"1H NMR konnte nicht erzeugt werden: {e}")

    with tab3:
        st.subheader("IR")
        try:
            fig3 = generator2.simulate_ir(
                smiles,
                seed=42,
                plot=False,
                show_title=show_structure,
            )
            st.pyplot(fig3, clear_figure=True)
        except Exception as e:
            st.error(f"IR konnte nicht erzeugt werden: {e}")

    with tab4:
        st.subheader("Elementaranalyse")
        try:
            result = generator5.elementaranalyse(smiles)
            if result:
                for el, perc in sorted(result.items()):
                    st.write(f"**{el}**: {perc:.2f} %")
            else:
                st.warning("Keine EA-Daten verfügbar.")
        except Exception as e:
            st.error(f"EA konnte nicht berechnet werden: {e}")

    if show_structure:
        with tab5:
            st.subheader("Struktur")
            try:
                img = smiles_to_pil(smiles)
                if img is not None:
                    st.image(img, width=320)
                else:
                    st.warning("Strukturbild konnte nicht erzeugt werden.")
            except Exception as e:
                    st.error(f"Struktur konnte nicht gezeichnet werden: {e}")


def render_home():
    st.title("Spektren Quiz")
    st.write("Trainiere die Zuordnung organischer Moleküle anhand simulierter Spektren.")

    col1, col2 = st.columns(2)

    with col2:
        card("Quiz", "Zufälliges Molekül aus der Hauptliste.")
        if st.button("Quiz starten", type="primary", use_container_width=True):
            mol = pick_random_molecule(moleküle)
            start_quiz(mol)
            st.rerun()

    with col1:
        card("Daily Quiz", "Jeden Tag ein neues Molekül.")
        if st.button("Daily Quiz öffnen", use_container_width=True):
            mol = pick_daily_molecule(moleküle_daily)
            start_daily(mol)
            st.rerun()

    with st.expander("Molekül nachschlagen", expanded=False):
        selected_name = st.selectbox("Name auswählen", [""] + namen_liste)
        smiles_input = st.text_input("Oder SMILES eingeben")

        if st.button("Nachschlagen", use_container_width=True):
            chosen_smiles = None

            if selected_name:
                chosen_smiles = name_to_smiles.get(selected_name.lower())

            elif smiles_input.strip():
                if molecule_exists(smiles_input.strip()):
                    chosen_smiles = smiles_input.strip()
                else:
                    st.error("Ungültiger SMILES.")
                    return

            else:
                st.warning("Bitte Namen auswählen oder SMILES eingeben.")
                return

            set_lookup(chosen_smiles)
            st.rerun()

    st.markdown("---")
    st.info(
        "Diese Anwendung dient der didaktischen Simulation chemischer Spektren. "
        "Die dargestellten Daten sind modellbasiert und ersetzen keine experimentellen Messdaten. "
        "Es wird keine Gewähr für Richtigkeit oder Vollständigkeit übernommen.\n\n"
        "Kontakt: deine.email@beispiel.de"
    )


def render_quiz():
    smiles = st.session_state["quiz_smiles"]
    correct_name = st.session_state["quiz_name"]

    if not smiles:
        st.warning("Kein Quiz aktiv.")
        if st.button("Zur Startseite"):
            go_home()
            st.rerun()
        return

    st.title("Quiz")
    render_spectra_tabs(smiles, show_structure=False)

    answer = st.selectbox(
        "Welches Molekül ist das?",
        [""] + namen_liste,
        key="quiz_answer_select",
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Abgeben", type="primary", use_container_width=True):
            correct = is_correct_answer(answer, smiles, name_to_smiles)
            submit_quiz(correct)
            st.rerun()

    with col2:
        if st.button("Zurück zur Startseite", use_container_width=True):
            go_home()
            st.rerun()

    if st.session_state["quiz_submitted"]:
        st.markdown("---")

        if st.session_state["quiz_correct"]:
            st.success(f"Richtig. Das Molekül war **{correct_name}**.")
        else:
            st.error(f"Falsch. Richtig war **{correct_name}**.")

        try:
            img = smiles_to_pil(smiles)
            if img is not None:
                st.image(img, caption=correct_name, width=320)
        except Exception as e:
            st.warning(f"Struktur konnte nicht angezeigt werden: {e}")

        col_a, col_b = st.columns(2)

        with col_a:
            if st.button("Noch ein Quiz", use_container_width=True):
                mol = pick_random_molecule(moleküle)
                start_quiz(mol)
                st.rerun()

        with col_b:
            if st.button("Startseite", use_container_width=True, key="quiz_home_end"):
                go_home()
                st.rerun()


def render_daily():
    st.title("Daily Quiz")

    today = date.today().isoformat()

    if st.session_state["daily_done_date"] == today:
        st.success("Du hast das Daily Quiz heute bereits abgeschlossen.")
        if st.button("Zur Startseite", key="daily_done_home"):
            go_home()
            st.rerun()
        return

    smiles = st.session_state["daily_smiles"]
    correct_name = st.session_state["daily_name"]

    if not smiles:
        mol = pick_daily_molecule(moleküle_daily)
        start_daily(mol)
        smiles = st.session_state["daily_smiles"]
        correct_name = st.session_state["daily_name"]

    render_spectra_tabs(smiles, show_structure=False)

    answer = st.selectbox(
        "Welches Molekül ist das heute?",
        [""] + daily_names,
        key="daily_answer_select",
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Daily abgeben", type="primary", use_container_width=True):
            correct = is_correct_answer(answer, smiles, daily_name_to_smiles)
            submit_daily(correct)
            st.rerun()

    with col2:
        if st.button("Zurück zur Startseite", key="daily_home_top", use_container_width=True):
            go_home()
            st.rerun()

    if st.session_state["daily_submitted"]:
        st.markdown("---")

        if st.session_state["daily_correct"]:
            st.success(f"Richtig. Das heutige Molekül war **{correct_name}**.")
        else:
            st.error(f"Falsch. Das heutige Molekül war **{correct_name}**.")

        try:
            img = smiles_to_pil(smiles)
            if img is not None:
                st.image(img, caption=correct_name, width=320)
        except Exception as e:
            st.warning(f"Struktur konnte nicht angezeigt werden: {e}")

        if st.button("Startseite", key="daily_home_bottom", use_container_width=True):
            go_home()
            st.rerun()


def render_lookup():
    smiles = st.session_state["lookup_smiles"]

    st.title("Molekül nachschlagen")

    if not smiles:
        st.warning("Kein Molekül ausgewählt.")
        if st.button("Zur Startseite", key="lookup_home_empty"):
            go_home()
            st.rerun()
        return

    st.write(f"**SMILES:** `{smiles}`")
    render_spectra_tabs(smiles, show_structure=True)

    if st.button("Zur Startseite", key="lookup_home", use_container_width=True):
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
