from __future__ import annotations
import streamlit as st
from datetime import date

from liste_neu import moleküle
from daily_molekuele import moleküle_daily

import generator
import generator2
import generator5
# import hnmr

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
    reset_quiz_state,
    reset_daily_state,
    go_home,
)

st.set_page_config(
    page_title="Spektren Quiz",
    page_icon="🧪",
    layout="wide",
)

init_session_state()

namen_liste, name_to_smiles, smiles_to_name = build_name_maps(moleküle)
daily_names, daily_name_to_smiles, daily_smiles_to_name = build_name_maps(moleküle_daily)


def render_spectra_tabs(smiles: str, show_structure: bool = True):
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["13C NMR", "1H NMR", "IR", "EA", "Struktur"])

    with tab1:
        st.subheader("13C NMR")
        try:
            fig1 = generator.simulate_13c_nmr(
                smiles,
                seed=42,
                plot=False,
                show_title=True,
                easymode=False,
            )
            st.pyplot(fig1, clear_figure=True)
        except Exception as e:
            st.error(f"13C NMR konnte nicht erzeugt werden: {e}")

    with tab2:
        st.subheader("1H NMR")
        st.info("Hier wird später deine 1H-NMR-Funktion eingebunden.")
        # Beispiel:
        # fig2 = hnmr.simulate_1h_nmr(smiles, seed=42, plot=False, show_title=True)
        # st.pyplot(fig2, clear_figure=True)

    with tab3:
        st.subheader("IR")
        try:
            fig3 = generator2.simulate_ir(smiles, seed=42, plot=False, show_title=True)
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

    with tab5:
        st.subheader("Struktur")
        if show_structure:
            img = smiles_to_pil(smiles)
            if img is not None:
                st.image(img, use_container_width=False)
            else:
                st.warning("Strukturbild konnte nicht erzeugt werden.")


def render_home():
    st.title("🧪 Spektren Quiz")
    st.write("Trainiere die Zuordnung organischer Moleküle anhand simulierter Spektren.")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Quiz")
        st.write("Zufälliges Molekül aus der Hauptliste. Beliebig oft wiederholbar.")
        if st.button("Quiz starten", use_container_width=True, type="primary"):
            mol = pick_random_molecule(moleküle)
            st.session_state["quiz_smiles"] = mol["smiles"]
            st.session_state["quiz_name"] = mol["name"]
            st.session_state["quiz_submitted"] = False
            st.session_state["quiz_correct"] = None
            st.session_state["mode"] = "quiz"
            st.rerun()

    with col2:
        st.markdown("### Daily Quiz")
        st.write("Ein tägliches Molekül aus einer separaten Liste. Kein 'Nochmal' am selben Tag.")
        if st.button("Daily Quiz öffnen", use_container_width=True):
            reset_daily_state()
            st.session_state["mode"] = "daily"
            st.rerun()

    with st.expander("Molekül nachschlagen", expanded=False):
        selected_name = st.selectbox(
            "Name auswählen",
            options=[""] + namen_liste,
            index=0,
        )
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

            st.session_state["lookup_smiles"] = chosen_smiles
            st.session_state["mode"] = "lookup"
            st.rerun()

    st.markdown("---")
    st.info(
        "Diese Anwendung dient der didaktischen Simulation chemischer Spektren. "
        "Die dargestellten Daten sind modellbasiert und ersetzen keine experimentellen Messdaten. "
        "Es wird keine Gewähr für Richtigkeit oder Vollständigkeit übernommen.\n\n"
        "Kontakt: deine.email@beispiel.de"
    )


def render_quiz():
    st.title("Quiz")

    smiles = st.session_state.get("quiz_smiles")
    if not smiles:
        st.warning("Kein Quiz aktiv.")
        if st.button("Zur Startseite"):
            go_home()
            st.rerun()
        return

    render_spectra_tabs(smiles, show_structure=False)

    answer = st.selectbox(
        "Welches Molekül ist das?",
        options=[""] + namen_liste,
        index=0,
    )

    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        if st.button("Abgeben", type="primary", use_container_width=True):
            correct = is_correct_answer(answer, smiles, name_to_smiles)
            st.session_state["quiz_submitted"] = True
            st.session_state["quiz_correct"] = correct
            st.rerun()

    with col2:
        if st.button("Zurück", use_container_width=True):
            go_home()
            st.rerun()

    if st.session_state.get("quiz_submitted"):
        correct = st.session_state.get("quiz_correct")
        correct_name = smiles_to_name.get(smiles.lower(), "Unbekannt")

        st.markdown("---")
        if correct:
            st.success(f"Richtig. Das Molekül war **{correct_name}**.")
        else:
            st.error(f"Falsch. Richtig war **{correct_name}**.")

        img = smiles_to_pil(smiles)
        if img is not None:
            st.image(img, caption=correct_name, width=300)

        col_a, col_b = st.columns(2)

        with col_a:
            if st.button("Noch ein Quiz", use_container_width=True):
                mol = pick_random_molecule(moleküle)
                st.session_state["quiz_smiles"] = mol["smiles"]
                st.session_state["quiz_name"] = mol["name"]
                st.session_state["quiz_submitted"] = False
                st.session_state["quiz_correct"] = None
                st.rerun()

        with col_b:
            if st.button("Startseite", use_container_width=True):
                go_home()
                st.rerun()


def render_daily():
    st.title("Daily Quiz")

    today = date.today().isoformat()

    if st.session_state.get("daily_done_date") == today:
        st.success("Du hast das Daily Quiz heute bereits abgeschlossen.")
        if st.button("Zur Startseite"):
            go_home()
            st.rerun()
        return

    daily_mol = pick_daily_molecule(moleküle_daily)
    daily_smiles = daily_mol["smiles"]
    daily_name = daily_mol["name"]

    render_spectra_tabs(daily_smiles, show_structure=False)

    answer = st.selectbox(
        "Welches Molekül ist das heute?",
        options=[""] + daily_names,
        index=0,
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Daily abgeben", type="primary", use_container_width=True):
            correct = is_correct_answer(answer, daily_smiles, daily_name_to_smiles)
            st.session_state["daily_submitted"] = True
            st.session_state["daily_correct"] = correct
            st.session_state["daily_done_date"] = today
            st.rerun()

    with col2:
        if st.button("Zurück", use_container_width=True):
            go_home()
            st.rerun()

    if st.session_state.get("daily_submitted"):
        st.markdown("---")
        if st.session_state.get("daily_correct"):
            st.success(f"Richtig. Das heutige Molekül war **{daily_name}**.")
        else:
            st.error(f"Falsch. Das heutige Molekül war **{daily_name}**.")

        img = smiles_to_pil(daily_smiles)
        if img is not None:
            st.image(img, caption=daily_name, width=300)

        if st.button("Startseite", use_container_width=True):
            go_home()
            st.rerun()


def render_lookup():
    st.title("Molekül nachschlagen")

    smiles = st.session_state.get("lookup_smiles")
    if not smiles:
        st.warning("Kein Molekül ausgewählt.")
        if st.button("Zur Startseite"):
            go_home()
            st.rerun()
        return

    st.write(f"**SMILES:** `{smiles}`")
    render_spectra_tabs(smiles, show_structure=True)

    if st.button("Zur Startseite", use_container_width=True):
        go_home()
        st.rerun()


mode = st.session_state.get("mode", "home")

if mode == "home":
    render_home()
elif mode == "quiz":
    render_quiz()
elif mode == "daily":
    render_daily()
elif mode == "lookup":
    render_lookup()
else:
    render_home()