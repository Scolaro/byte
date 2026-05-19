import streamlit as st

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

/* Make bordered containers stretch to 100% of their column height */
div[data-testid="column"] {
    display: flex;
    flex-direction: column;
}
div[data-testid="column"] > div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"] {
    flex-grow: 1;
    display: flex;
    flex-direction: column;
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
    import math
    if math.isinf(amount):
        return "∞"
    formatted = f"{amount:,.2f}"
    return formatted.replace(",", "X").replace(".", ",").replace("X", ".")


row1_col1, row1_col2 = st.columns(2)

with row1_col2:
    with st.container(border=True):
        st.header("2. Das Alte Haus (Vermietung)")

        r4c1, r4c2, r4c3 = st.columns(3)
        with r4c1:
            monthly_rent = st.number_input("Monatliche Mieteinnahmen", value=1400, step=None)
        with r4c2:
            renovations_old = st.number_input("Reparaturen vor Vermietung", value=20000, step=None)
        with r4c3:
            tax_rate_rent = st.number_input("Pausch. Steuersatz Mieterträge (%)", value=25.0, step=None, help="Puffer für die Einkommensteuer auf den Netto-Mietüberschuss. In der Realität greift hier Ihr persönlicher Grenzsteuersatz.")

        r4a_1, r4a_2 = st.columns(2)
        with r4a_1:
            afa_old_house = st.number_input("Jährliche Gebäudeabschreibung (AfA) in € 📌", value=3699.13, step=None, help="Mindert die Steuerlast, aber nicht den Cashflow.")
        with r4a_2:
            mietausfallwagnis_percent = st.number_input("Mietausfallwagnis (%)", value=2.5, step=None, help="Simuliert Leerstand und Mieterwechsel.")

        yearly_rent = monthly_rent * 12
        rent_result_placeholder = st.empty()


with row1_col1:
    with st.container(border=True):
        st.header("1. Das Neue Haus (Kauf)")

        r1c1, r1c2, r1c3 = st.columns(3)
        with r1c1:
            purchase_price = st.number_input("Kaufpreis (€)", value=600000, step=None)
        with r1c2:
            closing_costs_percent = st.number_input("Kaufnebenkosten (%)", value=8.0, step=None, help="In Hessen beträgt die Grunderwerbsteuer 6%. Notar und Grundbuchamt machen ca. 2% aus.")
        with r1c3:
            renovations_new = st.number_input("Reparaturen vor Einzug", value=25000, step=None)

        r1a1, r1a2, r1a3 = st.columns(3)
        with r1a1:
            down_payment = st.number_input("Eigenkapital (€)", value=160000, step=None, help="Bargeld, das Sie für den Kauf, die Nebenkosten und Renovierungen einsetzen.")
        with r1a2:
            wohnflaeche_new = st.number_input("Wohnfläche (m²)", value=150, step=None)
        with r1a3:
            pass

        closing_costs_eur = purchase_price * (closing_costs_percent / 100)
        total_capital_needed = purchase_price + closing_costs_eur + renovations_new + renovations_old
        loan_amount = total_capital_needed - down_payment

        r2c1, r2c2, r2c3, r2c4 = st.columns(4)
        with r2c1:
            st.markdown(f'<div class="calculated-result" style="margin-top: 10px;">Benötigtes Kapital: <b>€{format_eur(total_capital_needed)}</b></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="calculated-result">Benötigter Kreditbetrag: <b>€{format_eur(loan_amount)}</b></div>', unsafe_allow_html=True)
        with r2c2:
            st.markdown(f'<div class="calculated-result" style="margin-top: 10px;">Kaufnebenkosten: <b>€{format_eur(closing_costs_eur)}</b></div>', unsafe_allow_html=True)
        with r2c3:
            pass
        with r2c4:
            pass


# --- ROW 2: Laufende Nebenkosten ---
row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    with st.container(border=True):
        st.header("Laufende Nebenkosten (Jahr)")

        nk1c1, nk1c2, nk1c3, nk1c4 = st.columns(4)
        with nk1c1:
            nk_versicherung_new = st.number_input("Wohngebäudevers.", value=1000, step=None, key="nk_vers_new")
        with nk1c2:
            nk_grundsteuer_new = st.number_input("Grundsteuer", value=550, step=None, key="nk_gs_new")
        with nk1c3:
            nk_muell_new = st.number_input("Müll/Straßenreinigung", value=200, step=None, key="nk_muell_new")
        with nk1c4:
            nk_wasser_new = st.number_input("Wasser/Kanal/Niederschlag", value=525, step=None, key="nk_wasser_new", help="Wasser, Kanalgebühren & Niederschlagswasser")

        nk2c1, nk2c2, nk2c3, nk2c4 = st.columns(4)
        with nk2c1:
            nk_schornstein_new = st.number_input("Schornsteinfeger/Heizung", value=300, step=None, key="nk_schorn_new")
        with nk2c2:
            nk_verbrauch_new = st.number_input("Verbrauchskosten", value=4020, step=None, key="nk_verbr_new")
        with nk2c3:
            pass
        with nk2c4:
            pass

        yearly_nebenkosten_new = nk_versicherung_new + nk_grundsteuer_new + nk_muell_new + nk_wasser_new + nk_schornstein_new + nk_verbrauch_new
        monthly_nebenkosten_new = yearly_nebenkosten_new / 12

        nk3c1, nk3c2, nk3c3, nk3c4 = st.columns(4)
        with nk3c1:
            st.markdown(f'<div class="calculated-result">Jährliche Nebenkosten: <b>€{format_eur(yearly_nebenkosten_new)}</b></div>', unsafe_allow_html=True)
        with nk3c2:
            st.markdown(f'<div class="calculated-result">Monatliche Nebenkosten: <b>€{format_eur(monthly_nebenkosten_new)}</b></div>', unsafe_allow_html=True)
        with nk3c3:
            pass
        with nk3c4:
            pass

    with st.container(border=True):
        st.header("Hypotheken-Details")
        h4c1, h4c2, h4c3, h4c4 = st.columns(4)
        with h4c1:
            interest_rate = st.number_input("Zinssatz (%)", value=3.5, step=None)
        with h4c2:
            tilgungssatz = st.number_input("Anfängl. Tilgung (%)", value=2.0, step=None)
        with h4c3:
            zinsbindung = st.number_input("Zinsbindung (Jahre)", value=15, step=None)
        with h4c4:
            sondertilgung = st.number_input("Jährl. Sondertilgung (€)", value=0, step=None)

        if loan_amount <= 0:
            actual_monthly_payment = 0.0
            st.success("Ihr Eigenkapital deckt alle Kosten! Keine Hypothek erforderlich.")
        else:
            r = interest_rate / 100
            t = tilgungssatz / 100
            monthly_interest = r / 12
            actual_monthly_payment = (loan_amount * (r + t)) / 12

            current_balance = loan_amount
            months_passed = 0
            balance_at_fixed_end = loan_amount
            max_months = 1200 # 100 years max loop to prevent infinite hangs

            while current_balance > 0 and months_passed < max_months:
                interest_payment = current_balance * monthly_interest

                # If payment covers the rest, pay it off
                if current_balance + interest_payment <= actual_monthly_payment:
                    current_balance = 0
                    months_passed += 1
                    if months_passed == int(zinsbindung * 12):
                        balance_at_fixed_end = current_balance
                    break

                principal_payment = actual_monthly_payment - interest_payment

                if principal_payment <= 0 and sondertilgung <= 0:
                    months_passed = float('inf')
                    break

                current_balance -= principal_payment
                months_passed += 1

                if months_passed % 12 == 0:
                    current_balance -= sondertilgung

                current_balance = max(0, current_balance)

                if months_passed == int(zinsbindung * 12):
                    balance_at_fixed_end = current_balance

            if months_passed < int(zinsbindung * 12):
                balance_at_fixed_end = 0

            total_years = months_passed / 12 if months_passed != float('inf') else float('inf')

            hc_res1, hc_res2, hc_res3 = st.columns(3)
            with hc_res1:
                st.markdown(f'<div class="calculated-result" style="margin-top: 10px;">Erforderliche monatliche Rate: <b>€{format_eur(actual_monthly_payment)}</b></div>', unsafe_allow_html=True)
            with hc_res2:
                st.markdown(f'<div class="calculated-result" style="margin-top: 10px;">Restschuld nach {int(zinsbindung)} Jahren: <b>€{format_eur(balance_at_fixed_end)}</b></div>', unsafe_allow_html=True)
            with hc_res3:
                st.markdown(f'<div class="calculated-result" style="margin-top: 10px;">Geschätzte Gesamtlaufzeit: <b>{format_eur(total_years)} Jahre</b></div>', unsafe_allow_html=True)


with row2_col2:
    with st.container(border=True):
        st.header("Laufende Nebenkosten (Jahr)")

        nko1c1, nko1c2, nko1c3, nko1c4 = st.columns(4)
        with nko1c1:
            nk_haftpflicht_old = st.number_input("Haftpflicht 📌", value=100, step=None, key="nk_haft_old", help="Dieser Wert ist typischerweise vorgegeben, kann aber von Ihnen angepasst werden.")
        with nko1c2:
            nk_versicherung_old = st.number_input("Wohngebäudevers. 📌", value=1100, step=None, key="nk_vers_old", help="Dieser Wert ist typischerweise vorgegeben, kann aber von Ihnen angepasst werden.")
        with nko1c3:
            nk_grundsteuer_old = st.number_input("Grundsteuer 📌", value=430, step=None, key="nk_gs_old", help="Dieser Wert ist typischerweise vorgegeben, kann aber von Ihnen angepasst werden.")
        with nko1c4:
            nk_muell_old = st.number_input("Müll/Straßenreinigung 📌", value=200, step=None, key="nk_muell_old", help="Dieser Wert ist typischerweise vorgegeben, kann aber von Ihnen angepasst werden.")

        nko2c1, nko2c2, nko2c3, nko2c4 = st.columns(4)
        with nko2c1:
            nk_wasser_old = st.number_input("Wasser/Kanal/Niederschlag 📌", value=525, step=None, key="nk_wasser_old", help="Wasser, Kanalgebühren & Niederschlagswasser. Dieser Wert ist typischerweise vorgegeben, kann aber von Ihnen angepasst werden.")
        with nko2c2:
            nk_schornstein_old = st.number_input("Schornsteinfeger/Heizung 📌", value=300, step=None, key="nk_schorn_old", help="Dieser Wert ist typischerweise vorgegeben, kann aber von Ihnen angepasst werden.")
        with nko2c3:
            nk_verbrauch_old = st.number_input("Verbrauchskosten 📌", value=4020, step=None, key="nk_verbr_old", help="Dieser Wert ist typischerweise vorgegeben, kann aber von Ihnen angepasst werden.")
        with nko2c4:
            pass

        yearly_nebenkosten_old = nk_haftpflicht_old + nk_versicherung_old + nk_grundsteuer_old + nk_muell_old + nk_wasser_old + nk_schornstein_old + nk_verbrauch_old
        monthly_nebenkosten_old = yearly_nebenkosten_old / 12

        nko3c1, nko3c2, nko3c3, nko3c4 = st.columns(4)
        with nko3c1:
            st.markdown(f'<div class="calculated-result">Jährliche Nebenkosten: <b>€{format_eur(yearly_nebenkosten_old)}</b></div>', unsafe_allow_html=True)
        with nko3c2:
            st.markdown(f'<div class="calculated-result">Monatliche Nebenkosten: <b>€{format_eur(monthly_nebenkosten_old)}</b></div>', unsafe_allow_html=True)
        with nko3c3:
            pass
        with nko3c4:
            pass

        real_monthly_rent = monthly_rent * (1 - (mietausfallwagnis_percent / 100))
        monthly_afa_old = afa_old_house / 12

        tax_base = real_monthly_rent - monthly_afa_old
        if tax_base > 0:
            rental_tax = tax_base * (tax_rate_rent / 100)
        else:
            rental_tax = 0.0

        # The net rental cash flow is the real rent minus the taxes paid
        net_rental_surplus = real_monthly_rent - rental_tax

        with rent_result_placeholder.container():
            r4_res1, r4_res2, r4_res3 = st.columns(3)
            with r4_res1:
                st.markdown(f'<div class="calculated-result" style="margin-top: 10px;">Jährliche Mieteinnahmen (Kaltmiete): <b>€{format_eur(yearly_rent)}</b></div>', unsafe_allow_html=True)
            with r4_res2:
                help_icon_svg = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="currentColor" xmlns="http://www.w3.org/2000/svg" color="inherit" style="width: 1rem; height: 1rem; margin-left: 4px; vertical-align: middle; color: rgba(49, 51, 63, 0.6);"><path fill="none" d="M0 0h24v24H0V0z"></path><path d="M11 18h2v-2h-2v2zm1-16C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm0-14c-2.21 0-4 1.79-4 4h2c0-1.1.9-2 2-2s2 .9 2 2c0 2-3 1.75-3 5h2c0-2.25 3-2.5 3-5 0-2.21-1.79-4-4-4z"></path></svg>'
                st.markdown(f'<div class="calculated-result" style="margin-top: 10px;">Netto-Mietüberschuss (mtl., nach Steuerabzug) <span title="Miete - Mietausfallwagnis - Steuern" style="cursor: help;">{help_icon_svg}</span>: <b>€{format_eur(net_rental_surplus)}</b></div>', unsafe_allow_html=True)
            with r4_res3:
                pass

    with st.container(border=True):
        st.header("Einkommen")
        r5c1, r5c2 = st.columns(2)
        with r5c1:
            job_salary_net = st.number_input("Monatliches Netto-Gehalt (€) 📌", value=2600, step=None, help="Dieser Wert ist typischerweise vorgegeben, kann aber von Ihnen angepasst werden.")
        with r5c2:
            other_income = st.number_input("Andere Einkommensquellen (€)", value=0, step=None)

        total_monthly_income = job_salary_net + other_income

        r6c1, r6c2 = st.columns(2)
        with r6c1:
            st.markdown(f'<div class="calculated-result" style="margin-top: 10px;">Gesamtes jährliches Einkommen: <b>€{format_eur(total_monthly_income * 12)}</b></div>', unsafe_allow_html=True)
        with r6c2:
            st.markdown(f'<div class="calculated-result" style="margin-top: 10px;">Gesamtes monatliches Einkommen: <b>€{format_eur(total_monthly_income)}</b></div>', unsafe_allow_html=True)


# --- ROW 3: Stacked Left Column vs Finanzielle Analyse Right Column ---
row3_col1, row3_col2 = st.columns(2)

with row3_col1:
    with st.container(border=True):
        st.header("Laufende Kosten (Privat, mtl.)")
        pr1c1, pr1c2, pr1c3 = st.columns(3)
        with pr1c1:
            priv_nahrung = st.number_input("Nahrungsmittel", value=400, step=None)
        with pr1c2:
            priv_mobilitaet = st.number_input("Mobilität (Auto, ÖPNV)", value=300, step=None)
        with pr1c3:
            priv_versicherungen = st.number_input("Versicherungen", value=150, step=None)

        pr2c1, pr2c2, pr2c3 = st.columns(3)
        with pr2c1:
            priv_kommunikation = st.number_input("Kommunikation", value=60, step=None, help="Internet, Handy, etc.")
        with pr2c2:
            priv_sonstiges = st.number_input("Sonstiges", value=100, step=None)
        with pr2c3:
            pass

        monthly_nebenkosten_privat = priv_nahrung + priv_mobilitaet + priv_versicherungen + priv_kommunikation + priv_sonstiges

        pr3c1, pr3c2, pr3c3 = st.columns(3)
        with pr3c1:
            st.markdown(f'<div class="calculated-result" style="margin-top: 10px;">Jährliche Privatkosten: <b>€{format_eur(monthly_nebenkosten_privat * 12)}</b></div>', unsafe_allow_html=True)
        with pr3c2:
            st.markdown(f'<div class="calculated-result" style="margin-top: 10px;">Monatliche Privatkosten: <b>€{format_eur(monthly_nebenkosten_privat)}</b></div>', unsafe_allow_html=True)
        with pr3c3:
            pass

    with st.container(border=True):
        st.header("Private Sparraten / Rücklagen (mtl.)")
        sr1, sr2 = st.columns(2)
        with sr1:
            inst_new_house = st.number_input("Instandhaltungsrücklage Neues Haus", value=50, step=None, help="Sollte ca. 1-2 € pro m² pro Monat betragen")
        with sr2:
            inst_old_house = st.number_input("Instandhaltungsrücklage Altes Haus", value=50, step=None, help="Sollte ca. 1-2 € pro m² pro Monat betragen")

        total_monthly_savings = inst_new_house + inst_old_house


with row3_col2:
    with st.container(border=True):
        st.header("Finanzielle Analyse 💰")

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
        st.write("Vergleich der Ausgaben mit Ihrem Einkommen und den versteuerten Einnahmen aus dem alten Haus.")

        cf_col1, cf_col2 = st.columns(2)

        with cf_col1:
            st.subheader("Szenario A (Vermietet)")

            # Scenario A: deduct both savings rates
            net_monthly_cash_flow_a = total_monthly_income + net_rental_surplus - total_monthly_burden - total_monthly_savings
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

            # Scenario B: empty house means no rent, owner pays old house Nebenkosten, and still saves
            net_monthly_cash_flow_b = total_monthly_income - total_monthly_burden - monthly_nebenkosten_old - total_monthly_savings
            net_yearly_cash_flow_b = net_monthly_cash_flow_b * 12

            box_class_b = "cashflow-positive" if net_monthly_cash_flow_b >= 0 else "cashflow-negative"
            st.markdown(f"""
            <div class="cashflow-box {box_class_b}">
                <div class="cashflow-label">Netto Cashflow</div>
                <div class="cashflow-value">€{format_eur(net_monthly_cash_flow_b)}</div>
            </div>
            """, unsafe_allow_html=True)
            st.write(f"**Jährlicher Netto Cashflow:** €{format_eur(net_yearly_cash_flow_b)}")

# --- ROW 4: Bank-Risikoprüfung ---
st.markdown("---")
row4_col1, row4_col2 = st.columns(2)

with row4_col1:
    with st.container(border=True):
        st.header("Bank-Risikoprüfung 🏦")

        # 1. Beleihungsauslauf (LTV)
        ltv = loan_amount / purchase_price if purchase_price > 0 else 0
        ltv_pct = ltv * 100
        ltv_color = "green" if ltv_pct < 60 else "orange" if ltv_pct <= 80 else "red"

        # 2. Wohnkostenquote (Kapitaldienstgrenze)
        wkq = actual_monthly_payment / total_monthly_income if total_monthly_income > 0 else 0
        wkq_pct = wkq * 100
        wkq_color = "green" if wkq_pct <= 30 else "orange" if wkq_pct <= 40 else "red"

        # 3. Bewirtschaftungspauschale
        bewirtschaftung_pauschale = wohnflaeche_new * 2.5

        # 4. Zins- und Tilgungsanteil (für den 1. Monat)
        zins_anteil_1m = loan_amount * (interest_rate / 100 / 12)
        tilgung_anteil_1m = actual_monthly_payment - zins_anteil_1m

        b1, b2 = st.columns(2)
        with b1:
            st.markdown(f"**Beleihungsauslauf (LTV):** <span style='color:{ltv_color}; font-weight:bold;'>{format_eur(ltv_pct)} %</span>", unsafe_allow_html=True)
            st.markdown(f"**Wohnkostenquote:** <span style='color:{wkq_color}; font-weight:bold;'>{format_eur(wkq_pct)} %</span>", unsafe_allow_html=True)
        with b2:
            st.markdown(f"**Bewirtschaftungspauschale:** €{format_eur(bewirtschaftung_pauschale)}", unsafe_allow_html=True)
            st.markdown(f"**1. Monat Zins / Tilgung:** €{format_eur(zins_anteil_1m)} / €{format_eur(tilgung_anteil_1m)}", unsafe_allow_html=True)

with row4_col2:
    pass
