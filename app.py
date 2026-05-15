import streamlit as st
import numpy_financial as npf

st.set_page_config(page_title="Hausprojekt-Rechner", layout="wide")

st.title("🏡 Hausprojekt-Rechner")
st.write("Ermitteln Sie die finanzielle Machbarkeit des Kaufs eines neuen Hauses zur Eigennutzung, während Sie Ihr aktuelles Haus vermieten.")

# Inject some custom CSS to make it prettier and handle the custom cashflow box
st.markdown("""
<style>
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

def format_eur(amount):
    """Format numbers into German EUR style, e.g., 1.000,00"""
    # Use standard python formatting for grouping by comma, then swap comma and period
    formatted = f"{amount:,.2f}"
    # Replace standard grouping comma with a temp char, decimal period with comma, temp char with period
    return formatted.replace(",", "X").replace(".", ",").replace("X", ".")

# Layout
col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.header("1. Das Neue Haus")

        st.subheader("Kauf & Initiale Kosten")
        purchase_price = st.number_input("Kaufpreis (€)", value=500000, step=10000)

        st.write("**Kaufnebenkosten**")
        # Grunderwerbsteuer in Hesse is 6%, Notary ~2% -> Let's default to 8% total without Makler
        closing_costs_percent = st.number_input("Kaufnebenkosten (%)", value=8.0, step=0.1, help="In Hessen beträgt die Grunderwerbsteuer 6%. Notar und Grundbuchamt machen ca. 2% aus.")
        closing_costs_eur = purchase_price * (closing_costs_percent / 100)
        st.write(f"Berechnete Kaufnebenkosten: **€{format_eur(closing_costs_eur)}**")

        renovations_new = st.number_input("Geschätzte Reparaturen/Renovierungen für das neue Haus (€)", value=25000, step=5000)
        down_payment = st.number_input("Eigenkapital (€)", value=160000, step=5000, help="Bargeld, das Sie für den Kauf, die Nebenkosten und Renovierungen einsetzen.")

        total_capital_needed = purchase_price + closing_costs_eur + renovations_new
        loan_amount = total_capital_needed - down_payment

        st.write(f"Gesamt benötigtes Kapital: **€{format_eur(total_capital_needed)}**")
        st.write(f"Benötigter Kreditbetrag: **€{format_eur(loan_amount)}**")

        st.subheader("Hypotheken-Details")
        interest_rate = st.number_input("Zinssatz der Hypothek (%)", value=3.5, step=0.1)
        duration_years = st.number_input("Laufzeit der Hypothek (Jahre)", value=15, step=1)
        desired_monthly_payment = st.number_input("Gewünschte monatliche Rate (€)", value=1500, step=100)

        st.markdown("---")
        st.subheader("Laufende Nebenkosten (pro Jahr)")
        nk_versicherung_new = st.number_input("Wohngebäudeversicherung (€)", value=800, step=50, key="nk_vers_new")
        nk_grundsteuer_new = st.number_input("Grundsteuer (€)", value=600, step=50, key="nk_gs_new")
        nk_muell_new = st.number_input("Müllabfuhr/Straßenreinigung (€)", value=200, step=20, key="nk_muell_new")
        nk_wasser_new = st.number_input("Abwasser/Niederschlagswasser (€)", value=200, step=20, key="nk_wasser_new")
        nk_schornstein_new = st.number_input("Schornsteinfeger & Heizungswartung (€)", value=300, step=50, key="nk_schorn_new")
        nk_verbrauch_new = st.number_input("Verbrauchskosten (Heizung, Strom, Wasser) (€)", value=5000, step=100, key="nk_verbr_new")
        nk_instandhaltung_new = st.number_input("Instandhaltungsrücklage (€)", value=4320, step=100, key="nk_inst_new")

        yearly_nebenkosten_new = nk_versicherung_new + nk_grundsteuer_new + nk_muell_new + nk_wasser_new + nk_schornstein_new + nk_verbrauch_new + nk_instandhaltung_new
        monthly_nebenkosten_new = yearly_nebenkosten_new / 12

        st.write(f"Jährliche Nebenkosten: **€{format_eur(yearly_nebenkosten_new)}**")
        st.write(f"Monatliche Nebenkosten: **€{format_eur(monthly_nebenkosten_new)}**")


with col2:
    with st.container(border=True):
        st.header("2. Das Alte Haus (Vermietung)")

        st.subheader("Mieteinnahmen")
        monthly_rent = st.number_input("Erwartete monatliche Mieteinnahmen (Kaltmiete) (€)", value=1400, step=50)

        st.subheader("Renovierungen & Steuerabzüge")
        renovations_old = st.number_input("Reparaturen/Renovierungen vor Vermietung (€)", value=20000, step=1000)
        marginal_tax_rate = st.slider("Ihr Grenzsteuersatz (%)", min_value=15, max_value=45, value=42, step=1, help="Wird zur Berechnung Ihrer Steuerersparnis verwendet. In Deutschland liegt der Spitzensteuersatz bei 42% (oder 45% für sehr hohe Einkommen).")

        st.markdown("---")
        st.subheader("Laufende Nebenkosten (pro Jahr)")
        nk_haftpflicht_old = st.number_input("Haus- und Grundbesitzerhaftpflicht (€)", value=100, step=10, key="nk_haft_old")
        nk_grundsteuer_old = st.number_input("Grundsteuer (€)", value=430, step=50, key="nk_gs_old")
        nk_muell_old = st.number_input("Müllabfuhr/Straßenreinigung (€)", value=200, step=20, key="nk_muell_old")
        nk_wasser_old = st.number_input("Abwasser/Niederschlagswasser (€)", value=200, step=20, key="nk_wasser_old")
        nk_schornstein_old = st.number_input("Schornsteinfeger & Heizungswartung (€)", value=300, step=50, key="nk_schorn_old")
        nk_verbrauch_old = st.number_input("Verbrauchskosten (Heizung, Strom, Wasser) (€)", value=5000, step=100, key="nk_verbr_old")
        nk_instandhaltung_old = st.number_input("Instandhaltungsrücklage (€)", value=4320, step=100, key="nk_inst_old")

        yearly_nebenkosten_old = nk_haftpflicht_old + nk_grundsteuer_old + nk_muell_old + nk_wasser_old + nk_schornstein_old + nk_verbrauch_old + nk_instandhaltung_old
        monthly_nebenkosten_old = yearly_nebenkosten_old / 12

        st.write(f"Jährliche Nebenkosten: **€{format_eur(yearly_nebenkosten_old)}**")
        st.write(f"Monatliche Nebenkosten: **€{format_eur(monthly_nebenkosten_old)}**")

        st.markdown("---")
        st.subheader("Finanzen des alten Hauses (Vermietung)")

        yearly_rent = monthly_rent * 12
        st.write(f"Jährliche Mieteinnahmen (Kaltmiete): **€{format_eur(yearly_rent)}**")

        # Tax Deductions
        tax_savings = renovations_old * (marginal_tax_rate / 100)
        net_renovation_cost = renovations_old - tax_savings

        st.write(f"Geschätzte Steuerersparnis durch Renovierungen: **€{format_eur(tax_savings)}**")
        st.write(f"Nettokosten der Renovierungen (nach Steuern): **€{format_eur(net_renovation_cost)}**")

        with st.expander("ℹ️ Wie funktionieren Steuerabzüge für das alte Haus in Deutschland?"):
            st.write(f"""
            In Deutschland können Kosten, die für die Instandhaltung oder Reparatur einer vermieteten Immobilie anfallen (Erhaltungsaufwand), als *Werbungskosten* von Ihren Mieteinnahmen abgezogen werden.

            Da Ihr Grenzsteuersatz auf **{marginal_tax_rate}%** festgelegt ist, verringern Sie für jede 1.000 €, die Sie für Reparaturen ausgeben, Ihr zu versteuerndes Einkommen um 1.000 € und sparen so effektiv €{format_eur(1000 * marginal_tax_rate/100)} an Steuern.

            *Hinweis: Übersteigen die Renovierungskosten innerhalb der ersten 3 Jahre nach Anschaffung 15% des Gebäudewerts (anschaffungsnaher Herstellungsaufwand), müssen diese über 50 Jahre mit 2% pro Jahr abgeschrieben werden. Da Sie dieses Haus jedoch bereits besitzen und bewohnt haben, ist ein sofortiger Abzug für Instandhaltung und Reparaturen in der Regel anwendbar.*
            """)


# Layout for sections 3 and 4
col3, col4 = st.columns(2)

with col3:
    with st.container(border=True):
        st.header("3. Finanzielle Analyse & Grenzwert")
        # Calculations for New House Mortgage
        if loan_amount <= 0:
            st.success("Ihr Eigenkapital deckt alle Kosten! Keine Hypothek erforderlich.")
        else:
            # Monthly interest rate
            monthly_interest_rate = (interest_rate / 100) / 12
            total_months = duration_years * 12

            # Calculate the required monthly payment to zero out the loan
            actual_monthly_payment = -npf.pmt(monthly_interest_rate, total_months, loan_amount)

            st.subheader("Kosten für das Neue Haus")

            total_monthly_burden = actual_monthly_payment + monthly_nebenkosten_new

            inner_col1, inner_col2 = st.columns(2)
            with inner_col1:
                st.metric("Tatsächlich erforderliche monatliche Rate (Kredit)", f"€{format_eur(actual_monthly_payment)}")
            with inner_col2:
                st.metric("Gewünschte monatliche Rate", f"€{format_eur(desired_monthly_payment)}")

            st.write(f"Zuzüglich monatlicher Nebenkosten (**€{format_eur(monthly_nebenkosten_new)}**) ergibt sich eine Gesamte monatliche Belastung von **€{format_eur(total_monthly_burden)}**.")

            deficit = total_monthly_burden - desired_monthly_payment

            if deficit > 0:
                st.error(f"⚠️ **Defizit festgestellt**: Die tatsächliche Belastung (inkl. Nebenkosten) ist jeden Monat um €{format_eur(deficit)} höher als Ihre gewünschte Rate.")
            else:
                surplus = desired_monthly_payment - total_monthly_burden
                st.success(f"✅ **Grenzwert erreicht**: Ihre gewünschte Rate ist ausreichend! Sie haben einen Überschuss von €{format_eur(surplus)} pro Monat.")

            st.markdown("---")
            st.subheader("Zielpreis des Hauses")
            # Calculate target house price to exactly meet the "desired monthly payment" (after subtracting Nebenkosten from budget)
            budget_for_loan = desired_monthly_payment - monthly_nebenkosten_new
            if budget_for_loan > 0:
                target_loan_capacity = npf.pv(monthly_interest_rate, total_months, -budget_for_loan, 0)
                target_purchase_price_base = target_loan_capacity + down_payment - renovations_new
                target_purchase_price = target_purchase_price_base / (1 + (closing_costs_percent / 100))
                st.write(f"Damit Ihre **gewünschte Gesamtrate von €{format_eur(desired_monthly_payment)}** exakt ausreicht (unter Berücksichtigung der Nebenkosten und Beibehaltung aller anderen Angaben), dürfte das neue Haus maximal **€{format_eur(target_purchase_price)}** kosten.")
            else:
                st.write("Ihre gewünschte Rate reicht nicht aus, um die monatlichen Nebenkosten zu decken, daher ist kein Budget für einen Kredit vorhanden.")

with col4:
    with st.container(border=True):
        st.header("4. Gesamter Cashflow-Übersicht")
        st.write("Kombination der Kosten, Einnahmen und Ihres Einkommens.")

        job_salary_net = st.number_input("Monatliches Netto-Gehalt (€)", value=2400, step=100, help="Ihr monatliches Nettoeinkommen aus Ihrem Job, das in Ihren Cashflow einbezogen werden soll.")

        if loan_amount > 0:
            net_monthly_cash_flow = monthly_rent + job_salary_net - total_monthly_burden
            net_yearly_cash_flow = net_monthly_cash_flow * 12

            st.subheader("Monatliche Übersicht")
            inner_col3, inner_col4, inner_col5 = st.columns(3)
            inner_col3.metric("Mieteinnahmen", f"+ €{format_eur(monthly_rent)}")
            inner_col4.metric("Netto-Gehalt", f"+ €{format_eur(job_salary_net)}")
            inner_col5.metric("Belastung Neues Haus (inkl. NK)", f"- €{format_eur(total_monthly_burden)}")

            # Colored Box for Final Cash Flow
            box_class = "cashflow-positive" if net_monthly_cash_flow >= 0 else "cashflow-negative"
            st.markdown(f"""
            <div class="cashflow-box {box_class}">
                <div class="cashflow-label">Netto Monatlicher Cashflow</div>
                <div class="cashflow-value">€{format_eur(net_monthly_cash_flow)}</div>
            </div>
            """, unsafe_allow_html=True)

            st.write(f"**Jährlicher Netto Cashflow:** €{format_eur(net_yearly_cash_flow)}")

            st.info(f"""
            **Wie die Nebenkosten im Cashflow berechnet werden:**
            - Die Nebenkosten für das **neue Haus** (€{format_eur(monthly_nebenkosten_new)} monatlich) werden von Ihrem Cashflow abgezogen, da Sie diese selbst tragen müssen.
            - Die Nebenkosten für das **alte Haus** (€{format_eur(monthly_nebenkosten_old)} monatlich) werden *nicht* abgezogen, da davon ausgegangen wird, dass diese vom Mieter als Umlage bezahlt werden.
            - ⚠️ **Mietausfall-Risiko:** Falls das alte Haus leer steht, müssen Sie die Nebenkosten sowie den Mietausfall selbst tragen. Sie sollten daher einen Puffer in Höhe von mindestens **€{format_eur(monthly_rent + monthly_nebenkosten_old)} monatlich** einplanen.
            """)

            # Calculate affordability threshold
            max_affordable_payment = desired_monthly_payment + monthly_rent
            max_loan_budget = max_affordable_payment - monthly_nebenkosten_new

            st.subheader("Maximaler Erschwinglichkeits-Grenzwert")
            if max_loan_budget > 0:
                max_loan_capacity = npf.pv(monthly_interest_rate, total_months, -max_loan_budget, 0)
                max_purchase_price = max_loan_capacity + down_payment - renovations_new
                max_purchase_price = max_purchase_price / (1 + (closing_costs_percent / 100))
                st.write(f"Basierend auf Ihrer gewünschten Rate von **€{format_eur(desired_monthly_payment)}** PLUS den Mieteinnahmen von **€{format_eur(monthly_rent)}** (Gesamteinnahmen: €{format_eur(max_affordable_payment)}), abzüglich der Nebenkosten für das neue Haus, können Sie ein Haus für bis zu **€{format_eur(max_purchase_price)}** kaufen.")
            else:
                st.write("Die Kombination aus gewünschter Rate und Mieteinnahmen reicht nicht aus, um die Nebenkosten des neuen Hauses zu decken.")
