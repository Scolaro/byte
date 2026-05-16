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
- **Mieteinnahmen:** Die monatliche Kaltmiete, die Sie vom Mieter erhalten.
- **Reparaturen vor Vermietung:** Diese Kosten werden direkt auf den neuen Kreditbetrag aufgeschlagen, da sie in der Regel zeitnah zum Auszug anfallen.
- **Steuern:** Mieteinnahmen sind steuerpflichtig. Wir ziehen von der Kaltmiete zunächst die nicht-umlagefähigen Kosten (wie die Instandhaltungsrücklage) ab und versteuern den verbleibenden Überschuss mit dem von Ihnen gewählten Pauschalsatz. Nur dieser **Netto-Mietüberschuss** fließt positiv in Ihren Cashflow ein.

### 3. Laufende Nebenkosten
Für beide Häuser erfassen Sie hier die jährlichen Betriebskosten.
- **Neues Haus:** Diese Kosten tragen Sie in voller Höhe selbst. (Hinweis: Als Selbstnutzer benötigen Sie hier keine spezielle Grundbesitzerhaftpflicht, da dies meist über die private Haftpflicht abgedeckt ist).
- **Altes Haus:** Bei Vermietung (Szenario A) werden die umlagefähigen Kosten über die Nebenkostenabrechnung vom Mieter getragen. Sie müssen lediglich die Instandhaltungsrücklage von der Miete abziehen. Steht das Haus jedoch leer (Szenario B), fallen *alle* Kosten (inklusive der Haus- und Grundbesitzerhaftpflicht) auf Sie zurück.

### 4. Einkommen & Privatkosten
Damit der Cashflow realistisch ist, betrachten wir Ihr verfügbares Budget:
- Ihr **monatliches Netto-Gehalt** und **weitere Einkommensquellen** bilden die Basis.
- Davon abgezogen werden die **Laufenden Kosten (Privat)** wie Nahrungsmittel, Versicherungen und Sonstiges.

### 5. Finanzielle Analyse (Szenarien)
Die abschließende Analyse führt alle Ausgaben und Einnahmen zusammen, um Ihren Netto-Cashflow zu ermitteln.

Die **Gesamte monatliche Belastung** setzt sich zusammen aus der Kreditrate für das neue Haus, den Nebenkosten des neuen Hauses und Ihren privaten Lebenshaltungskosten.

* **Szenario A (Vermietet):**
  Ihr Einkommen wird um den *versteuerten Netto-Mietüberschuss* ergänzt. Davon ziehen wir die gesamte monatliche Belastung ab.

* **Szenario B (Leerstand):**
  Das alte Haus bringt keine Mieteinnahmen. Ihr Einkommen muss nun die gesamte monatliche Belastung **sowie zusätzlich** die vollen monatlichen Nebenkosten des leerstehenden alten Hauses tragen.

Sollte der Cashflow-Wert rot sein, übersteigen Ihre monatlichen Ausgaben Ihre Einnahmen.
""")
