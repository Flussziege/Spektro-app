Ich entwickle eine Streamlit-App für ein Spektroskopie-Quiz (¹H-NMR, ¹³C-NMR, IR sind bereits implementiert). Jetzt möchte ich ein **Massenspektrum (MS)** Modul hinzufügen.

Bitte hilf mir, eine saubere, realistische, aber vereinfachte MS-Simulation zu implementieren.

## Kontext der App

* Backend: Python
* UI: Streamlit
* Moleküle kommen als **SMILES**
* RDKit ist bereits integriert
* Spektren werden als **Plotly-Figuren** dargestellt (interaktiv)
* Struktur:

  * Simulationen passieren in separaten Modulen (z. B. `generator.py`, `hnmr.py`)
  * Rendering erfolgt in `render_spectra_tabs()`
  * MS soll dort als neuer Tab erscheinen

---

## Ziel des MS-Moduls

Ich möchte ein **didaktisches, vereinfachtes Massenspektrum**, kein perfektes physikalisches Modell.

Das MS soll:

1. **Molekülion (M⁺)** anzeigen
2. Typische **Fragmente generieren**
3. **relative Intensitäten** darstellen
4. als **Stick-Spektrum (m/z vs Intensität)** geplottet werden
5. deterministisch sein (Seed steuerbar, wie bei NMR)

---

## Gewünschte Funktion

Bitte implementiere eine Funktion:

```python
def simulate_ms(smiles: str, seed: int = 42) -> dict:
```

### Output-Format:

```python
{
    "peaks": [
        {"mz": float, "intensity": float, "label": str}
    ]
}
```

Optional:

```python
"molecular_ion": float
```

---

## Anforderungen an die Simulation

### 1. Molekülmasse

* Bestimme die **monoisotopische Masse** aus SMILES (RDKit)
* Das ist das **M⁺-Peak**

---

### 2. Fragmentierung (vereinfacht!)

Baue eine regelbasierte Logik:

#### Typische Fragmentierungen:

* **C–C Spaltung**
* **α-Spaltung neben Heteroatomen (O, N)**
* **Verlust von kleinen Gruppen**

  * H₂O (–18)
  * CO (–28)
  * CO₂ (–44)
  * CH₃ (–15)

#### Optional:

* Stabilere Fragmente → höhere Intensität
* z. B.:

  * tertiäre Cationen > sekundäre > primäre
  * aromatische Fragmente stabiler

---

### 3. Intensitäten

* Normiere Intensitäten auf max = 100
* Molekülion darf z. B.:

  * schwach sein (z. B. 10–40)
* Base Peak = 100

---

### 4. Rauschen / Realismus

Optional:

* kleine zufällige Peaks
* leichte Variation durch `seed`

---

## Plotting (sehr wichtig)

Ich brauche zusätzlich eine Funktion:

```python
def make_interactive_ms_plot(ms_result: dict) -> plotly.graph_objects.Figure
```

### Anforderungen:

* x-Achse: m/z
* y-Achse: Intensität (%)
* Darstellung:

  * **Stick-Spektrum (vertikale Linien)**
* Hover:

  * m/z
  * Intensität
  * Label (falls vorhanden)
* Styling:

  * kompatibel mit Dark/Light Mode
  * ähnlich wie meine anderen Spektren

---

## Integration in meine App

Das MS wird in `render_spectra_tabs()` eingebunden:

```python
elif key == "ms":
    st.subheader(t("ms_title"))

    ms_result = simulate_ms(smiles)
    fig = make_interactive_ms_plot(ms_result)

    st.plotly_chart(fig, width="stretch")
```

---

## Zusätzliche Wünsche

* Code soll modular sein (eigene Datei z. B. `ms_simulator.py`)
* gut kommentiert
* leicht erweiterbar
* keine unnötige Komplexität
* im lookup soll man über peaks hover können und diese fragmente werden dann angezeigt/ tauchen als kleines bild auf

---

## Was ich NICHT brauche

* keine perfekte physikalische MS-Simulation
* keine extrem komplexe Fragmentierungschemie

---

## Was ich WILL

* klare Struktur
* gute Heuristiken
* nachvollziehbares Verhalten (für Lernzwecke)
* isotopenmuster

---

Bitte:

lass uns erstmal über das konzept und die funktionweise, sowie due funktionen nachdenken, bervor wir code schreiben