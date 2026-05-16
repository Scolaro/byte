import streamlit as st
import numpy_financial as npf

# Must be the first Streamlit command
st.set_page_config(page_title="Hausprojekt-Rechner", layout="wide", initial_sidebar_state="collapsed")

# Inject custom CSS
st.markdown("""
<style>
/* Remove top padding */
.block-container {
    padding-top: 1rem;
    padding-bottom: 0rem;
}

/* Hide the sidebar completely */
[data-testid="collapsedControl"] {
    display: none;
}
[data-testid="stSidebar"] {
    display: none;
}

/* Hide Streamlit number input step up/down arrows natively */
div[data-testid="stNumberInputStepUp"] {
    display: none !important;
}
div[data-testid="stNumberInputStepDown"] {
    display: none !important;
}
input[type=number] {
    -moz-appearance: textfield;
}
input[type=number]::-webkit-inner-spin-button,
input[type=number]::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

/* Thicker borders for the st.container */
div[data-testid="stVerticalBlock"] > div[style*="border"] {
    border-width: 2px !important;
    border-radius: 8px !important;
}

/* Increase size of calculated results */
.calculated-result {
    font-size: 1.2rem;
    font-weight: 500;
    margin-bottom: 0.5rem;
}

div[data-testid="stMetricValue"] {
    font-size: 1.5rem;
}

.cashflow-box {
    border-radius: 0.5rem;
    padding: 1rem;
    margin-top: 1rem;
    text-align: center;
}
.cashflow-positive {
    background-color: #d1fae5;
    border: 2px solid #10b981;
    color: #065f46;
}
.cashflow-negative {
    background-color: #fee2e2;
    border: 2px solid #ef4444;
    color: #991b1b;
}
.cashflow-label {
    font-size: 1rem;
    font-weight: bold;
    margin-bottom: 0.5rem;
}
.cashflow-value {
    font-size: 2rem;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)


st.title("🏡 Hausprojekt-Rechner")

st.page_link("pages/1_Erklaerung.py", label="📖 Detaillierte Erklärung der Berechnungen anzeigen", icon="👉")

st.write("Ermitteln Sie die finanzielle Machbarkeit des Kaufs eines neuen Hauses zur Eigennutzung, während Sie Ihr aktuelles Haus vermieten.")

def format_eur(amount):
    """Format numbers into German EUR style, e.g., 1.000,00"""
    formatted = f"{amount:,.2f}"
    return formatted.replace(",", "X").replace(".", ",").replace("X", ".")


# --- WE EXTRACT ALL INPUTS FIRST WITHOUT UI LAYOUT SO WE CAN COMPUTE GLOBALLY ---

row1_col1, row1_col2 = st.columns(2)

with row1_col2:
    with st.container(border=True):
        st.header("2. Das Alte Haus (Vermietung)")

        r4c1, r4c2 = st.columns(2)
        with r4c1:
            monthly_rent = st.number_input("Monatliche Mieteinnahmen", value=1400, step=None)
        with r4c2:
            renovations_old = st.number_input("Reparaturen vor Vermietung", value=20000, step=None)

        yearly_rent = monthly_rent * 12
        st.markdown(f'<div class="calculated-result">Jährliche Mieteinnahmen (Kaltmiete): <b>€{format_eur(yearly_rent)}</b></div>', unsafe_allow_html=True)

        # Add vertical spacer to match the height of "Das Neue Haus" so that the next rows align perfectly
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")

with row1_col1:
    with st.container(border=True):
        st.header("1. Das Neue Haus (Kauf)")

        r1c1, r1c2, r1c3 = st.columns(3)
        with r1c1:
            purchase_price = st.number_input("Kaufpreis (€)", value=500000, step=None)
        with r1c2:
            closing_costs_percent = st.number_input("Kaufnebenkosten (%)", value=8.0, step=None, help="In Hessen beträgt die Grunderwerbsteuer 6%. Notar und Grundbuchamt machen ca. 2% aus.")
        with r1c3:
            renovations_new = st.number_input("Reparaturen vor Einzug", value=25000, step=None)

        # Calculate dynamic values now that renovations_old is available
        closing_costs_eur = purchase_price * (closing_costs_percent / 100)
        total_capital_needed = purchase_price + closing_costs_eur + renovations_new + renovations_old

        r2c1, r2c2, r2c3 = st.columns(3)
        with r2c1:
            st.markdown(f'<div class="calculated-result" style="margin-top: 32px;">Benötigtes Kapital: <b>€{format_eur(total_capital_needed)}</b></div>', unsafe_allow_html=True)

        with r2c2:
            st.markdown(f'<div class="calculated-result" style="margin-top: 32px;">Kaufnebenkosten: <b>€{format_eur(closing_costs_eur)}</b></div>', unsafe_allow_html=True)

        with r2c3:
            down_payment = st.number_input("Eigenkapital (€)", value=160000, step=None, help="Bargeld, das Sie für den Kauf, die Nebenkosten und Renovierungen einsetzen.")

        loan_amount = total_capital_needed - down_payment

        r3c1, r3c2, r3c3 = st.columns(3)
        with r3c1:
            st.markdown(f'<div class="calculated-result">Benötigter Kreditbetrag: <b>€{format_eur(loan_amount)}</b></div>', unsafe_allow_html=True)


# --- ROW 2: Laufende Nebenkosten ---
row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    with st.container(border=True):
        st.header("Laufende Nebenkosten (Jahr)")
        nk1c1, nk1c2, nk1c3 = st.columns(3)
        with nk1c1:
            nk_versicherung_new = st.number_input("Wohngebäudevers.", value=800, step=None, key="nk_vers_new")
        with nk1c2:
            nk_grundsteuer_new = st.number_input("Grundsteuer", value=600, step=None, key="nk_gs_new")
        with nk1c3:
            nk_muell_new = st.number_input("Müll/Straßenreinigung", value=200, step=None, key="nk_muell_new")

        nk2c1, nk2c2, nk2c3 = st.columns(3)
        with nk2c1:
            nk_wasser_new = st.number_input("Abwasser/Regen", value=200, step=None, key="nk_wasser_new")
        with nk2c2:
            nk_schornstein_new = st.number_input("Schornsteinfeger/Heizung", value=300, step=None, key="nk_schorn_new")
        with nk2c3:
            nk_verbrauch_new = st.number_input("Verbrauchskosten", value=5000, step=None, key="nk_verbr_new")

        yearly_nebenkosten_new = nk_versicherung_new + nk_grundsteuer_new + nk_muell_new + nk_wasser_new + nk_schornstein_new + nk_verbrauch_new

        nk3c1, nk3c2, nk3c3 = st.columns(3)
        with nk3c1:
            nk_instandhaltung_new = st.number_input("Instandhaltungsrücklage", value=500, step=None, key="nk_inst_new", help="Sollte ca. 1-2 € pro m² pro Monat betragen")

        yearly_nebenkosten_new = yearly_nebenkosten_new + nk_instandhaltung_new
        monthly_nebenkosten_new = yearly_nebenkosten_new / 12

        with nk3c2:
            st.markdown(f'<div class="calculated-result" style="margin-top: 32px;">Jährliche Nebenkosten: <b>€{format_eur(yearly_nebenkosten_new)}</b></div>', unsafe_allow_html=True)
        with nk3c3:
            st.markdown(f'<div class="calculated-result" style="margin-top: 32px;">Monatliche Nebenkosten: <b>€{format_eur(monthly_nebenkosten_new)}</b></div>', unsafe_allow_html=True)

with row2_col2:
    with st.container(border=True):
        st.header("Laufende Nebenkosten (Jahr)")
        nko1c1, nko1c2, nko1c3 = st.columns(3)
        with nko1c1:
            nk_haftpflicht_old = st.number_input("Haftpflicht 📌", value=100, step=None, key="nk_haft_old", help="Dieser Wert ist typischerweise vorgegeben, kann aber von Ihnen angepasst werden.")
        with nko1c2:
            nk_grundsteuer_old = st.number_input("Grundsteuer 📌", value=430, step=None, key="nk_gs_old", help="Dieser Wert ist typischerweise vorgegeben, kann aber von Ihnen angepasst werden.")
        with nko1c3:
            nk_muell_old = st.number_input("Müll/Straßenreinigung 📌", value=200, step=None, key="nk_muell_old", help="Dieser Wert ist typischerweise vorgegeben, kann aber von Ihnen angepasst werden.")

        nko2c1, nko2c2, nko2c3 = st.columns(3)
        with nko2c1:
            nk_wasser_old = st.number_input("Abwasser/Regen 📌", value=200, step=None, key="nk_wasser_old", help="Dieser Wert ist typischerweise vorgegeben, kann aber von Ihnen angepasst werden.")
        with nko2c2:
            nk_schornstein_old = st.number_input("Schornsteinfeger/Heizung 📌", value=300, step=None, key="nk_schorn_old", help="Dieser Wert ist typischerweise vorgegeben, kann aber von Ihnen angepasst werden.")
        with nko2c3:
            nk_verbrauch_old = st.number_input("Verbrauchskosten 📌", value=5000, step=None, key="nk_verbr_old", help="Dieser Wert ist typischerweise vorgegeben, kann aber von Ihnen angepasst werden.")

        yearly_nebenkosten_old = nk_haftpflicht_old + nk_grundsteuer_old + nk_muell_old + nk_wasser_old + nk_schornstein_old + nk_verbrauch_old

        nko3c1, nko3c2, nko3c3 = st.columns(3)
        with nko3c1:
            nk_instandhaltung_old = st.number_input("Instandhaltungsrücklage", value=500, step=None, key="nk_inst_old", help="Sollte ca. 1-2 € pro m² pro Monat betragen")

        yearly_nebenkosten_old = yearly_nebenkosten_old + nk_instandhaltung_old
        monthly_nebenkosten_old = yearly_nebenkosten_old / 12

        with nko3c2:
            st.markdown(f'<div class="calculated-result" style="margin-top: 32px;">Jährliche Nebenkosten: <b>€{format_eur(yearly_nebenkosten_old)}</b></div>', unsafe_allow_html=True)
        with nko3c3:
            st.markdown(f'<div class="calculated-result" style="margin-top: 32px;">Monatliche Nebenkosten: <b>€{format_eur(monthly_nebenkosten_old)}</b></div>', unsafe_allow_html=True)


# --- ROW 3: Stacked Left Column vs Finanzielle Analyse Right Column ---
row3_col1, row3_col2 = st.columns(2)

with row3_col1:
    with st.container(border=True):
        st.header("Hypotheken-Details")
        h4c1, h4c2 = st.columns(2)
        with h4c1:
            interest_rate = st.number_input("Zinssatz der Hypothek (%)", value=3.5, step=None)
        with h4c2:
            duration_years = st.number_input("Laufzeit der Hypothek (Jahre)", value=15, step=None)

        if loan_amount <= 0:
            actual_monthly_payment = 0.0
            st.success("Ihr Eigenkapital deckt alle Kosten! Keine Hypothek erforderlich.")
        else:
            monthly_interest_rate = (interest_rate / 100) / 12
            total_months = duration_years * 12
            actual_monthly_payment = -npf.pmt(monthly_interest_rate, total_months, loan_amount)

        st.markdown(f'<div class="calculated-result" style="margin-top: 10px;">Erforderliche monatliche Rate (Kredit): <b>€{format_eur(actual_monthly_payment)}</b></div>', unsafe_allow_html=True)

    with st.container(border=True):
        st.header("Einkommen")
        r5c1, r5c2 = st.columns(2)
        with r5c1:
            job_salary_net = st.number_input("Monatliches Netto-Gehalt (€) 📌", value=2400, step=None, help="Dieser Wert ist typischerweise vorgegeben, kann aber von Ihnen angepasst werden.")
        with r5c2:
            other_income = st.number_input("Andere Einkommensquellen (€)", value=0, step=None)

        total_monthly_income = job_salary_net + other_income
        st.markdown(f'<div class="calculated-result" style="margin-top: 10px;">Gesamtes monatliches Einkommen: <b>€{format_eur(total_monthly_income)}</b></div>', unsafe_allow_html=True)

    with st.container(border=True):
        st.header("Laufende Kosten (Privat)")
        pr1c1, pr1c2, pr1c3 = st.columns(3)
        with pr1c1:
            priv_nahrung = st.number_input("Nahrungsmittel", value=400, step=None)
        with pr1c2:
            priv_versicherungen = st.number_input("Versicherungen", value=200, step=None)
        with pr1c3:
            priv_sonstiges = st.number_input("Sonstiges", value=300, step=None)

        monthly_nebenkosten_privat = priv_nahrung + priv_versicherungen + priv_sonstiges
        st.markdown(f'<div class="calculated-result" style="margin-top: 10px;">Monatliche Privatkosten: <b>€{format_eur(monthly_nebenkosten_privat)}</b></div>', unsafe_allow_html=True)


with row3_col2:
    with st.container(border=True):
        st.header("Finanzielle Analyse")

        total_monthly_burden = actual_monthly_payment + monthly_nebenkosten_new + monthly_nebenkosten_privat

        st.subheader("Ausgaben (Monatlich)")

        ausg1, ausg2, ausg3 = st.columns(3)
        with ausg1:
            st.metric("Erforderliche Rate (Kredit)", f"€{format_eur(actual_monthly_payment)}")
        with ausg2:
            st.metric("Nebenkosten (Haus)", f"€{format_eur(monthly_nebenkosten_new)}")
        with ausg3:
            st.metric("Privatkosten", f"€{format_eur(monthly_nebenkosten_privat)}")

        st.markdown(f'<div class="calculated-result" style="margin-top:15px; font-size: 1.5rem;">Gesamte monatliche Belastung: <b>€{format_eur(total_monthly_burden)}</b></div>', unsafe_allow_html=True)

        st.markdown("---")

        st.write("Vergleich der Ausgaben mit Ihrem Einkommen und den Einnahmen aus dem alten Haus.")

        cf_col1, cf_col2 = st.columns(2)

        with cf_col1:
            st.subheader("Szenario A (Vermietet)")

            net_monthly_cash_flow_a = total_monthly_income + monthly_rent - total_monthly_burden
            net_yearly_cash_flow_a = net_monthly_cash_flow_a * 12

            box_class_a = "cashflow-positive" if net_monthly_cash_flow_a >= 0 else "cashflow-negative"
            st.markdown(f"""
            <div class="cashflow-box {box_class_a}">
                <div class="cashflow-label">Netto Cashflow</div>
                <div class="cashflow-value">€{format_eur(net_monthly_cash_flow_a)}</div>
            </div>
            """, unsafe_allow_html=True)
            st.write(f"**Jährlicher Netto Cashflow:** €{format_eur(net_yearly_cash_flow_a)}")

        with cf_col2:
            st.subheader("Szenario B (Leerstand)")

            net_monthly_cash_flow_b = total_monthly_income - total_monthly_burden - monthly_nebenkosten_old
            net_yearly_cash_flow_b = net_monthly_cash_flow_b * 12

            box_class_b = "cashflow-positive" if net_monthly_cash_flow_b >= 0 else "cashflow-negative"
            st.markdown(f"""
            <div class="cashflow-box {box_class_b}">
                <div class="cashflow-label">Netto Cashflow</div>
                <div class="cashflow-value">€{format_eur(net_monthly_cash_flow_b)}</div>
            </div>
            """, unsafe_allow_html=True)
            st.write(f"**Jährlicher Netto Cashflow:** €{format_eur(net_yearly_cash_flow_b)}")

        # Add vertical spacers so the single box matches the height of the 3 stacked boxes on the left
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")


# Add spacing at the bottom of the page
st.write("")
st.write("")
st.write("")
