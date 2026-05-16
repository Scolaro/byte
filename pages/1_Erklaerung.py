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
- **Erforderliche monatliche Rate (Kredit):** Anhand des Kreditbetrags, des Zinssatzes und der Laufzeit wird hier die monatliche Annuität (Zins + Tilgung) berechnet, die notwendig ist, um den Kredit in der angegebenen Laufzeit vollständig abzuzahlen.

### 2. Das Alte Haus (Vermietung)
Hier erfassen Sie die wirtschaftlichen Eckdaten Ihrer bestehenden Immobilie:
- **Mieteinnahmen:** Die monatliche Kaltmiete, die Sie vom Mieter erhalten.
- **Reparaturen vor Vermietung:** Diese Kosten werden, wie oben erwähnt, direkt auf den neuen Kreditbetrag aufgeschlagen, da sie in der Regel zeitnah zum Auszug aus dem alten Haus anfallen.

### 3. Laufende Nebenkosten
Für beide Häuser erfassen Sie hier die jährlichen Betriebskosten. Die Summe wird durch 12 geteilt, um die monatlichen Nebenkosten zu erhalten.
- **Neues Haus:** Diese Kosten tragen Sie in voller Höhe selbst.
- **Altes Haus:** Bei Vermietung (Szenario A) werden die meisten dieser Kosten (außer z. B. Instandhaltungsrücklage und Haftpflicht) typischerweise über die Nebenkostenabrechnung auf den Mieter umgelegt. Im Rechner gehen wir zur Vereinfachung davon aus, dass Sie bei Vermietung diese Kosten nicht aus dem eigenen Cashflow bestreiten müssen. Steht das Haus jedoch leer (Szenario B), fallen diese Kosten komplett auf Sie zurück.

### 4. Einkommen & Privatkosten
Damit der Cashflow realistisch ist, betrachten wir Ihr verfügbares Budget:
- Ihr **monatliches Netto-Gehalt** und **weitere Einkommensquellen** bilden die Basis.
- Davon abgezogen werden die **Laufenden Kosten (Privat)** wie Nahrungsmittel, Versicherungen und Sonstiges.

### 5. Finanzielle Analyse (Szenarien)
Die abschließende Analyse führt alle Ausgaben und Einnahmen zusammen, um Ihren Netto-Cashflow (das Geld, das am Ende des Monats auf dem Konto bleibt oder fehlt) zu ermitteln.

Die **Gesamte monatliche Belastung** setzt sich zusammen aus der Kreditrate für das neue Haus, den Nebenkosten des neuen Hauses und Ihren privaten Lebenshaltungskosten.

Davon ausgehend berechnen wir zwei Szenarien:

* **Szenario A (Vermietet):**
  Hier geht es im Idealfall reibungslos zu. Ihr Einkommen wird um die Mieteinnahmen des alten Hauses ergänzt. Davon ziehen wir die gesamte monatliche Belastung ab. Die Nebenkosten des alten Hauses tauchen hier nicht als Minus auf, da wir davon ausgehen, dass der Mieter diese zahlt (bzw. die Kaltmiete als reiner Gewinn verbucht wird).

* **Szenario B (Leerstand):**
  Dies ist das Worst-Case-Szenario. Das alte Haus bringt keine Mieteinnahmen. Ihr Einkommen muss nun die gesamte monatliche Belastung **sowie zusätzlich** die vollen monatlichen Nebenkosten des leerstehenden alten Hauses tragen.

Sollte der Cashflow-Wert rot sein, übersteigen Ihre monatlichen Ausgaben Ihre Einnahmen.
""")
