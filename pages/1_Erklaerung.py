import streamlit as st

st.set_page_config(page_title="Hausprojekt-Rechner: Erklärung", layout="wide", initial_sidebar_state="collapsed")

# Hide the sidebar completely
st.markdown("""
<style>
    [data-testid="collapsedControl"] {
        display: none;
    }
    [data-testid="stSidebar"] {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

st.title("📖 Funktionsweise & Berechnungen")

st.page_link("app.py", label="Zurück zum Hauptrechner", icon="🔙")

st.markdown("""
Diese Seite erklärt detailliert, wie der Hausprojekt-Rechner funktioniert, welche Annahmen getroffen werden und wie sich die Endergebnisse zusammensetzen.

### 1. Das Neue Haus (Kauf)
Hier wird der finanzielle Grundstein für Ihr neues Eigenheim gelegt:
- **Benötigtes Kapital:** Summiert den Kaufpreis, die prozentualen Kaufnebenkosten (wie Grunderwerbsteuer, Notar, Grundbuch), die Reparaturen vor dem Einzug ins neue Haus **sowie** die Reparaturen, die vor der Vermietung des alten Hauses anfallen.
- **Benötigter Kreditbetrag:** Dies ist das benötigte Kapital abzüglich Ihres eingesetzten Eigenkapitals. Dieser Betrag wird durch die Hypothek finanziert.
- **Erforderliche monatliche Rate (Kredit):** Berechnet nach der in Deutschland üblichen Methode für Annuitätenkredite. Die Rate ergibt sich aus dem gewünschten anfänglichen Tilgungssatz und dem Zinssatz: `(Kreditbetrag * (Zinssatz + Tilgungssatz)) / 12`.

### 2. Das Alte Haus (Vermietung)
Hier erfassen Sie die wirtschaftlichen Eckdaten Ihrer bestehenden Immobilie:
- **Mieteinnahmen & Mietausfallwagnis:** Die monatliche Kaltmiete wird um das von Ihnen angegebene Mietausfallwagnis reduziert. Dies simuliert realistische Einnahmeverluste durch Leerstand oder Mieterwechsel.
- **Reparaturen vor Vermietung:** Diese Kosten werden direkt auf den neuen Kreditbetrag aufgeschlagen, da sie in der Regel zeitnah zum Auszug anfallen. *(Tipp: Diese Renovierungskosten können in der Realität oft als sofort abziehbarer Erhaltungsaufwand von der Steuer abgesetzt werden und so in den ersten Jahren zu hohen Steuerrückerstattungen führen).*
- **Gebäudeabschreibung (AfA) & Steuern:** Mieteinnahmen sind steuerpflichtig. Die Steuerlast berechnet sich aus der realen Miete (Miete abzgl. Ausfallwagnis) abzüglich der Gebäudeabschreibung (AfA). Da die AfA eine reine Steuervergünstigung ist, verlässt das Geld nicht Ihr Konto.
- **Netto-Mietüberschuss:** Das ist der tatsächliche Betrag, der auf Ihrem Konto landet: Die reale Miete abzüglich der berechneten Steuern. Er fließt positiv in Ihren Cashflow ein.

### 3. Laufende Nebenkosten
Für beide Häuser erfassen Sie hier die jährlichen Betriebskosten.
- **Neues Haus:** Diese Kosten tragen Sie in voller Höhe selbst. (Hinweis: Als Selbstnutzer benötigen Sie hier keine spezielle Grundbesitzerhaftpflicht, da dies meist über die private Haftpflicht abgedeckt ist).
- **Altes Haus:** Bei Vermietung (Szenario A) werden die hier angegebenen umlagefähigen Kosten über die Nebenkostenabrechnung vom Mieter getragen und beeinflussen Ihren Cashflow nicht negativ. Steht das Haus jedoch leer (Szenario B), fallen *alle* Kosten (inklusive der Haus- und Grundbesitzerhaftpflicht) auf Sie zurück.
*Hinweis: Instandhaltungsrücklagen zählen zu den privaten Sparraten und werden getrennt berechnet.*

### 4. Einkommen, Privatkosten & Rücklagen
Damit der Cashflow realistisch ist, betrachten wir Ihr verfügbares Budget:
- Ihr **monatliches Netto-Gehalt** und **weitere Einkommensquellen** bilden die Basis.
- Davon abgezogen werden die **Laufenden Kosten (Privat)** wie Nahrungsmittel, Versicherungen und Sonstiges.
- Ebenfalls abgezogen werden die **Privaten Sparraten / Rücklagen** (wie z. B. die Instandhaltungsrücklagen für beide Häuser). Das garantiert, dass das Sparen für künftige Reparaturen aus Ihrem Netto-Einkommen bestritten wird.

### 5. Finanzielle Analyse (Szenarien)
Die abschließende Analyse führt alle Ausgaben und Einnahmen zusammen, um Ihren finalen Netto-Cashflow zu ermitteln.

Die **Gesamte monatliche Belastung** setzt sich zusammen aus der Kreditrate für das neue Haus, den Nebenkosten des neuen Hauses und Ihren privaten Lebenshaltungskosten.

* **Szenario A (Vermietet):**
  Ihr Einkommen wird um den *Netto-Mietüberschuss (nach Steuern)* ergänzt. Davon ziehen wir die gesamte monatliche Belastung sowie Ihre privaten Sparraten (Instandhaltung) ab.

* **Szenario B (Leerstand):**
  Das alte Haus bringt keine Mieteinnahmen. Ihr Einkommen muss nun die gesamte monatliche Belastung, Ihre privaten Sparraten **sowie zusätzlich** die vollen monatlichen Nebenkosten des leerstehenden alten Hauses tragen.

Sollte der Cashflow-Wert rot sein, übersteigen Ihre monatlichen Ausgaben Ihre Einnahmen.

### 6. Bank-Risikoprüfung
Hier sehen Sie die wichtigsten Kennzahlen, die Banken intern zur Kreditvergabe nutzen:
- **Beleihungsauslauf (LTV):** Prozentualer Anteil des Kaufpreises, der finanziert wird. (< 60% = Bestzinsen, > 80% = Risiko).
- **Wohnkostenquote:** Zeigt, wie viel Prozent Ihres Nettoeinkommens für die monatliche Kreditrate aufgewendet werden muss. (Sollte unter 30-40% liegen).
- **Bewirtschaftungspauschale:** Pauschaler Abzug der Bank für Nebenkosten (oft 2,50 € pro m²).
- **Zins- und Tilgungsanteil (1. Monat):** Zeigt auf einen Blick, wie viel Ihrer ersten Rate in Ihren Vermögensaufbau (Tilgung) und wie viel an die Bank (Zinsen) fließt.
""")
