import streamlit as st
import numpy_financial as npf

# Must be the first Streamlit command
st.set_page_config(page_title="Hausprojekt-Rechner", layout="wide")

# Inject some custom CSS to make it prettier, handle the custom cashflow box, adjust borders, and remove top whitespace
st.markdown("""
<style>
/* Remove top padding */
.block-container {
    padding-top: 1rem;
    padding-bottom: 0rem;
}

/* Thicker borders for the st.container */
div[data-testid="stVerticalBlock"] > div[style*="border"] {
    border-width: 2px !important;
    border-radius: 8px !important;
}

/* Increase size of calculated results (e.g. st.write results) */
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
st.write("Ermitteln Sie die finanzielle Machbarkeit des Kaufs eines neuen Hauses zur Eigennutzung, während Sie Ihr aktuelles Haus vermieten.")

def format_eur(amount):
    """Format numbers into German EUR style, e.g., 1.000,00"""
    formatted = f"{amount:,.2f}"
    return formatted.replace(",", "X").replace(".", ",").replace("X", ".")


# ROW 1: New House vs Old House
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    with st.container(border=True):
        st.header("1. Das Neue Haus")

        st.subheader("Kauf & Initiale Kosten")
        r1c1, r1c2 = st.columns(2)
        with r1c1:
            purchase_price = st.number_input("Kaufpreis (€)", value=500000, step=10000)
        with r1c2:
            closing_costs_percent = st.number_input("Kaufnebenkosten (%)", value=8.0, step=0.1, help="In Hessen beträgt die Grunderwerbsteuer 6%. Notar und Grundbuchamt machen ca. 2% aus.")

        closing_costs_eur = purchase_price * (closing_costs_percent / 100)
        st.markdown(f'<div class="calculated-result">Berechnete Kaufnebenkosten: <b>€{format_eur(closing_costs_eur)}</b></div>', unsafe_allow_html=True)

        r2c1, r2c2 = st.columns(2)
        with r2c1:
            renovations_new = st.number_input("Geschätzte Reparaturen", value=25000, step=5000)
        with r2c2:
            down_payment = st.number_input("Eigenkapital (€)", value=160000, step=5000, help="Bargeld, das Sie für den Kauf, die Nebenkosten und Renovierungen einsetzen.")

        total_capital_needed = purchase_price + closing_costs_eur + renovations_new
        loan_amount = total_capital_needed - down_payment

        st.markdown(f'<div class="calculated-result">Gesamt benötigtes Kapital: <b>€{format_eur(total_capital_needed)}</b></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="calculated-result">Benötigter Kreditbetrag: <b>€{format_eur(loan_amount)}</b></div>', unsafe_allow_html=True)

with row1_col2:
    with st.container(border=True):
        st.header("2. Das Alte Haus (Vermietung)")

        r4c1, r4c2 = st.columns(2)
        with r4c1:
            monthly_rent = st.number_input("Monatliche Mieteinnahmen", value=1400, step=50)
        with r4c2:
            renovations_old = st.number_input("Reparaturen vor Vermietung", value=20000, step=1000)

        yearly_rent = monthly_rent * 12
        st.markdown(f'<div class="calculated-result">Jährliche Mieteinnahmen (Kaltmiete): <b>€{format_eur(yearly_rent)}</b></div>', unsafe_allow_html=True)


# ROW 2: Laufende Nebenkosten
row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    with st.container(border=True):
        st.header("Laufende Nebenkosten (Neues Haus)")
        nk1c1, nk1c2, nk1c3 = st.columns(3)
        with nk1c1:
            nk_versicherung_new = st.number_input("Wohngebäudevers.", value=800, step=50, key="nk_vers_new")
        with nk1c2:
            nk_grundsteuer_new = st.number_input("Grundsteuer", value=600, step=50, key="nk_gs_new")
        with nk1c3:
            nk_muell_new = st.number_input("Müll/Straßenreinigung", value=200, step=20, key="nk_muell_new")

        nk2c1, nk2c2, nk2c3 = st.columns(3)
        with nk2c1:
            nk_wasser_new = st.number_input("Abwasser/Regen", value=200, step=20, key="nk_wasser_new")
        with nk2c2:
            nk_schornstein_new = st.number_input("Schornsteinfeger/Heizung", value=300, step=50, key="nk_schorn_new")
        with nk2c3:
            nk_verbrauch_new = st.number_input("Verbrauchskosten", value=5000, step=100, key="nk_verbr_new")

        nk3c1, nk3c2, nk3c3 = st.columns(3)
        with nk3c1:
            nk_instandhaltung_new = st.number_input("Instandhaltungsrücklage", value=500, step=100, key="nk_inst_new", help="Sollte ca. 1-2 € pro m² pro Monat betragen")

        yearly_nebenkosten_new = nk_versicherung_new + nk_grundsteuer_new + nk_muell_new + nk_wasser_new + nk_schornstein_new + nk_verbrauch_new + nk_instandhaltung_new
        monthly_nebenkosten_new = yearly_nebenkosten_new / 12

        st.markdown(f'<div class="calculated-result">Jährliche Nebenkosten: <b>€{format_eur(yearly_nebenkosten_new)}</b></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="calculated-result">Monatliche Nebenkosten: <b>€{format_eur(monthly_nebenkosten_new)}</b></div>', unsafe_allow_html=True)

with row2_col2:
    with st.container(border=True):
        st.header("Laufende Nebenkosten (Altes Haus)")
        nko1c1, nko1c2, nko1c3 = st.columns(3)
        with nko1c1:
            nk_haftpflicht_old = st.number_input("Haftpflicht", value=100, step=10, key="nk_haft_old")
        with nko1c2:
            nk_grundsteuer_old = st.number_input("Grundsteuer", value=430, step=50, key="nk_gs_old")
        with nko1c3:
            nk_muell_old = st.number_input("Müll/Straßenreinigung", value=200, step=20, key="nk_muell_old")

        nko2c1, nko2c2, nko2c3 = st.columns(3)
        with nko2c1:
            nk_wasser_old = st.number_input("Abwasser/Regen", value=200, step=20, key="nk_wasser_old")
        with nko2c2:
            nk_schornstein_old = st.number_input("Schornsteinfeger/Heizung", value=300, step=50, key="nk_schorn_old")
        with nko2c3:
            nk_verbrauch_old = st.number_input("Verbrauchskosten", value=5000, step=100, key="nk_verbr_old")

        nko3c1, nko3c2, nko3c3 = st.columns(3)
        with nko3c1:
            nk_instandhaltung_old = st.number_input("Instandhaltungsrücklage", value=500, step=100, key="nk_inst_old", help="Sollte ca. 1-2 € pro m² pro Monat betragen")

        yearly_nebenkosten_old = nk_haftpflicht_old + nk_grundsteuer_old + nk_muell_old + nk_wasser_old + nk_schornstein_old + nk_verbrauch_old + nk_instandhaltung_old
        monthly_nebenkosten_old = yearly_nebenkosten_old / 12

        st.markdown(f'<div class="calculated-result">Jährliche Nebenkosten: <b>€{format_eur(yearly_nebenkosten_old)}</b></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="calculated-result">Monatliche Nebenkosten: <b>€{format_eur(monthly_nebenkosten_old)}</b></div>', unsafe_allow_html=True)


# ROW 3: Hypotheken-Details vs Einkommen
row3_col1, row3_col2 = st.columns(2)

with row3_col1:
    with st.container(border=True):
        st.header("Hypotheken-Details")
        r3c1, r3c2 = st.columns(2)
        with r3c1:
            interest_rate = st.number_input("Zinssatz der Hypothek (%)", value=3.5, step=0.1)
        with r3c2:
            duration_years = st.number_input("Laufzeit der Hypothek (Jahre)", value=15, step=1)

        if loan_amount <= 0:
            actual_monthly_payment = 0.0
            st.success("Ihr Eigenkapital deckt alle Kosten! Keine Hypothek erforderlich.")
        else:
            monthly_interest_rate = (interest_rate / 100) / 12
            total_months = duration_years * 12
            actual_monthly_payment = -npf.pmt(monthly_interest_rate, total_months, loan_amount)

        st.markdown(f'<div class="calculated-result" style="margin-top: 10px;">Erforderliche monatliche Rate (Kredit): <b>€{format_eur(actual_monthly_payment)}</b></div>', unsafe_allow_html=True)


with row3_col2:
    with st.container(border=True):
        st.header("Einkommen")
        r5c1, r5c2 = st.columns(2)
        with r5c1:
            job_salary_net = st.number_input("Monatliches Netto-Gehalt (€)", value=2400, step=100, help="Ihr monatliches Nettoeinkommen.")
        with r5c2:
            other_income = st.number_input("Andere Einkommensquellen (monatlich) (€)", value=0, step=50)

        total_monthly_income = job_salary_net + other_income


# ROW 4: Finanzielle Analyse vs Cashflow
row4_col1, row4_col2 = st.columns(2)

with row4_col1:
    with st.container(border=True):
        st.header("3. Finanzielle Analyse")

        if loan_amount > 0:
            total_monthly_burden = actual_monthly_payment + monthly_nebenkosten_new

            st.subheader("Kosten für das Neue Haus")

            inner_col1, inner_col2 = st.columns(2)
            with inner_col1:
                st.metric("Erforderliche monatliche Rate (Kredit)", f"€{format_eur(actual_monthly_payment)}")
            with inner_col2:
                st.metric("Monatliche Nebenkosten", f"€{format_eur(monthly_nebenkosten_new)}")

            st.markdown(f'<div class="calculated-result" style="margin-top:15px; font-size: 1.5rem;">Gesamte monatliche Belastung: <b>€{format_eur(total_monthly_burden)}</b></div>', unsafe_allow_html=True)

with row4_col2:
    with st.container(border=True):
        st.header("4. Cashflow")
        st.write("Vergleich der Kosten für das neue Haus mit Ihrem Einkommen und den Einnahmen aus dem alten Haus.")

        total_monthly_burden = actual_monthly_payment + monthly_nebenkosten_new

        cf_col1, cf_col2 = st.columns(2)

        with cf_col1:
            st.subheader("Szenario A (Vermietet)")
            st.write("Die Nebenkosten des alten Hauses werden vom Mieter getragen.")

            net_monthly_cash_flow_a = total_monthly_income + monthly_rent - total_monthly_burden

            box_class_a = "cashflow-positive" if net_monthly_cash_flow_a >= 0 else "cashflow-negative"
            st.markdown(f"""
            <div class="cashflow-box {box_class_a}">
                <div class="cashflow-label">Netto Cashflow</div>
                <div class="cashflow-value">€{format_eur(net_monthly_cash_flow_a)}</div>
            </div>
            """, unsafe_allow_html=True)

        with cf_col2:
            st.subheader("Szenario B (Leerstand)")
            st.write("Sie tragen Hypothek **und** Nebenkosten beider Häuser.")

            net_monthly_cash_flow_b = total_monthly_income - total_monthly_burden - monthly_nebenkosten_old

            box_class_b = "cashflow-positive" if net_monthly_cash_flow_b >= 0 else "cashflow-negative"
            st.markdown(f"""
            <div class="cashflow-box {box_class_b}">
                <div class="cashflow-label">Netto Cashflow</div>
                <div class="cashflow-value">€{format_eur(net_monthly_cash_flow_b)}</div>
            </div>
            """, unsafe_allow_html=True)
