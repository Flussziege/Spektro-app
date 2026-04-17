# Prompt: Verbesserung der MS-Simulation (ms_simulator.py)

Du bekommst einen Python-Code zur Simulation von Elektronen-Ionisations-Massenspektren (EI-MS).
Der Code verwendet RDKit für die Molekülanalyse und generiert Peaks heuristisch.
Verbessere den Code nach den folgenden Anweisungen **ohne physikalische Simulation einzuführen**.
Alle Verbesserungen sind rein heuristischer Natur, basierend auf bekannten EI-MS-Fragmentierungsregeln.

---

## Änderung 1 — Alkyl-Ionen-Serie für aliphatische Moleküle

**Wo:** Neue Funktion `_generate_alkyl_series()`, aufgerufen in `simulate_ms()`.

**Warum:** Aliphatische Verbindungen (keine Aromaten, keine Carbonyle) zeigen charakteristische
CₙH₂ₙ₊₁⁺-Serien bei m/z 29, 43, 57, 71, 85... Diese fehlen komplett und sind diagnostisch wichtig.

**Wie:**
- Nur aufrufen wenn: `not features.has_aromatic and not features.carbonyl_like and features.carbon_count >= 5`
- Iteriere n von 2 bis `min(features.carbon_count - 1, 8)`
- Masse: `14.01565 * n + 1.00782` (= CₙH₂ₙ₊₁)
- Intensität: Nimmt mit steigendem n leicht ab: `base = 40.0 / (1 + 0.3 * (n - 2))`
- Kind: `"alkyl_series"`

---

## Änderung 2 — Acylium-Kationen (R–C≡O⁺)

**Wo:** Neue Funktion `_generate_acylium_peaks()`, aufgerufen in `simulate_ms()`.

**Warum:** Bei Ketonen, Aldehyden, Estern und Amiden entstehen durch α-Spaltung neben dem
Carbonyl charakteristische Acylium-Ionen (R–C≡O⁺). Das ist eines der diagnostisch wertvollsten
Signale in EI-Spektren und fehlt im aktuellen Code vollständig.

**Wie:**
- SMARTS: `"[CX3](=O)[#6]"` für Carbonyl-C mit angebundenem Kohlenstoff
- Für jeden Match: Spalte die C–C-Bindung neben dem Carbonyl
- Berechne Masse des Acylium-Fragments (der Teil mit C=O, Ladung durch fehlendes H)
- Intensität: `55.0` als Basis, wenn das Fragment aromatisch ist `+20`, wenn klein (≤4 Atome) `-10`
- Kind: `"acylium"`

---

## Änderung 3 — Intensitäts-Kompetition zwischen Peaks

**Wo:** Neue Funktion `_apply_intensity_competition()`, aufgerufen nach allen Peak-Generatoren,
vor `_merge_close_peaks()`.

**Warum:** Aktuell werden alle Intensitäten unabhängig berechnet. In der Realität konkurrieren
Fragmentierungswege — wenn ein Peak dominiert, werden andere geschwächt.

**Wie:**
- Finde den Peak mit der höchsten Intensität (`dominant`)
- Alle Peaks mit `intensity < 0.25 * dominant.intensity` werden mit Faktor `0.65` multipliziert
- Peaks mit `kind in ("noise", "isotope")` werden von dieser Regel ausgenommen
- Peaks mit `metadata.get("protected")` (aromatic_specials) werden ausgenommen

---

## Änderung 4 — Sekundäre Neutralverluste aus Fragmenten

**Wo:** In `_generate_second_generation_fragments()`, nach dem child-Peak erzeugt wurde.

**Warum:** Fragments mit OH, NH₂ oder COOH können ihrerseits nochmals H₂O (18), NH₃ (17)
oder CO (28) verlieren. Das erzeugt realistische Cluster von Peaks im Spektrum.

**Wie:**
- Nach Erzeugung jedes `child`-Peaks: Lade `child.fragment_smiles` als RDKit-Mol
- Wenn Fragment Alkohol hat: erzeuge zusätzlichen Peak bei `child.mz - 18.0106`,
  Intensität = `child.intensity * 0.35`, Label `"secondary H₂O loss"`, Kind `"secondary_loss"`
- Wenn Fragment primäres Amin hat: erzeuge Peak bei `child.mz - 17.0265`,
  Intensität = `child.intensity * 0.30`, Label `"secondary NH₃ loss"`, Kind `"secondary_loss"`
- Wenn Fragment Carbonyl hat: erzeuge Peak bei `child.mz - 27.9949`,
  Intensität = `child.intensity * 0.25`, Label `"secondary CO loss"`, Kind `"secondary_loss"`
- Nur hinzufügen wenn `mz > 10`

---

## Änderung 5 — Realistischeres Rauschen (exponentialverteiltes m/z)

**Wo:** In `_generate_noise_peaks()`.

**Warum:** Echtes Rauschen häuft sich bei niedrigen m/z. Die aktuelle Gleichverteilung
über den gesamten m/z-Bereich ist unrealistisch.

**Wie:**
- Erhöhe Standardanzahl von 2 auf 4 Peaks
- Erzeuge m/z mit: `mz = rng.expovariate(1.0 / (max_mz * 0.12)) + 14`
- Clamp auf `min(mz, max_mz * 0.45)` damit kein Rauschen nahe dem Molekülion liegt
- Intensität: `rng.uniform(1.5, 5.5)`

---

## Änderung 6 — Retro-Diels-Alder für Cyclohexen-artige Ringe

**Wo:** Neue Funktion `_generate_retro_da_peaks()`, aufgerufen in `simulate_ms()`.

**Warum:** Cyclohexen-Derivate zeigen charakteristischen Verlust von Butadien (54 Da) bzw.
Ethen (28 Da) durch Retro-Diels-Alder-Reaktion. Fehlt komplett.

**Wie:**
- SMARTS zur Erkennung: `"[#6]1~[#6]~[#6]=[#6]~[#6]~[#6]1"` (6-Ring mit Doppelbindung)
- Wenn Match: erzeuge Peak bei `M - 54.0470` (Butadien-Verlust), Intensität `~60`
- Optional: Peak bei `M - 28.0313` (Ethen-Verlust) mit Intensität `~35`
- Kind: `"retro_da"`
- Nur wenn Molekülmasse > 80 Da

---

## Änderung 7 — Molekülion-Intensität nach Stickstoffregel korrigieren

**Wo:** In `_generate_molecular_ion_peak()`.

**Warum:** Die Stickstoffregel besagt: ungerade Anzahl Stickstoffatome → ungerades Molekulargewicht.
Wichtiger: Verbindungen mit vielen Stickstoffatomen zeigen oft schwache M⁺-Peaks.

**Wie:**
- Wenn `features.hetero_counts["N"] >= 2`: `intensity *= 0.80`
- Wenn `features.hetero_counts["N"] == 0 and not features.has_aromatic`: `intensity *= 0.85`
  (rein aliphatisch, kein N → schlechte Ionenstabilität)

---

## Zu beachten

- Alle neuen Peaks kommen **vor** `_merge_close_peaks()` in die `all_peaks`-Liste
- `_apply_intensity_competition()` wird **nach** dem Zusammenführen aller Peaks aufgerufen,
  **vor** `_merge_close_peaks()`
- Die Signatur von `simulate_ms()` bleibt unverändert
- Das Rückgabeformat bleibt unverändert
- Neue `kind`-Werte werden in `peak_details` automatisch sichtbar
- Keine neuen externen Abhängigkeiten einführen (nur RDKit und stdlib)
