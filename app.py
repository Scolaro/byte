import streamlit as st
import numpy_financial as npf

st.set_page_config(page_title="Hausprojekt-Rechner", layout="wide")

st.title("🏡 Hausprojekt-Rechner (Hessen, Deutschland)")
st.write("Ermitteln Sie die finanzielle Machbarkeit des Kaufs eines neuen Hauses zur Eigennutzung, während Sie Ihr aktuelles Haus vermieten.")

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


with col2:
    with st.container(border=True):
        st.header("2. Das Alte Haus (Vermietung)")

        st.subheader("Mieteinnahmen")
        monthly_rent = st.number_input("Erwartete monatliche Mieteinnahmen (Kaltmiete) (€)", value=1400, step=50)

        st.subheader("Renovierungen & Steuerabzüge")
        renovations_old = st.number_input("Reparaturen/Renovierungen vor Vermietung (€)", value=20000, step=1000)
        marginal_tax_rate = st.slider("Ihr Grenzsteuersatz (%)", min_value=15, max_value=45, value=42, step=1, help="Wird zur Berechnung Ihrer Steuerersparnis verwendet. In Deutschland liegt der Spitzensteuersatz bei 42% (oder 45% für sehr hohe Einkommen).")

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


st.markdown("---")

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

        col3, col4 = st.columns(2)
        with col3:
            st.metric("Tatsächlich erforderliche monatliche Rate", f"€{format_eur(actual_monthly_payment)}")
        with col4:
            st.metric("Gewünschte monatliche Rate", f"€{format_eur(desired_monthly_payment)}")

        deficit = actual_monthly_payment - desired_monthly_payment

        if deficit > 0:
            st.error(f"⚠️ **Defizit festgestellt**: Die erforderliche Rate ist jeden Monat um €{format_eur(deficit)} höher als Ihre gewünschte Rate.")
        else:
            surplus = desired_monthly_payment - actual_monthly_payment
            st.success(f"✅ **Grenzwert erreicht**: Ihre gewünschte Rate ist ausreichend! Sie haben einen Überschuss von €{format_eur(surplus)} pro Monat.")


st.markdown("---")
with st.container(border=True):
    st.header("4. Gesamter Cashflow-Übersicht")
    st.write("Kombination der Kosten für das neue Haus, der Einnahmen aus dem alten Haus und Ihres persönlichen Einkommens.")

    job_salary_net = st.number_input("Monatliches Netto-Gehalt (€)", value=2400, step=100, help="Ihr monatliches Nettoeinkommen aus Ihrem Job, das in Ihren Cashflow einbezogen werden soll.")

    if loan_amount > 0:
        net_monthly_cash_flow = monthly_rent + job_salary_net - actual_monthly_payment
        net_yearly_cash_flow = (monthly_rent * 12) + (job_salary_net * 12) - (actual_monthly_payment * 12)

        st.subheader("Monatliche Übersicht")
        col5, col6, col8, col7 = st.columns(4)
        col5.metric("Mieteinnahmen", f"+ €{format_eur(monthly_rent)}")
        col6.metric("Netto-Gehalt", f"+ €{format_eur(job_salary_net)}")
        col8.metric("Hypothekenrate", f"- €{format_eur(actual_monthly_payment)}")
        col7.metric("Netto Monatlicher Cashflow", f"€{format_eur(net_monthly_cash_flow)}",
                    delta_color="normal" if net_monthly_cash_flow >= 0 else "inverse",
                    delta=f"€{format_eur(net_monthly_cash_flow)}")

        st.write(f"**Jährlicher Netto Cashflow:** €{format_eur(net_yearly_cash_flow)}")

        st.info("""
        **Verständnis des Ergebnisses:**
        - Wenn Ihr monatlicher Netto-Cashflow **positiv** ist, decken Ihre Mieteinnahmen Ihre gesamte neue Hypothek.
        - Wenn Ihr monatlicher Netto-Cashflow **negativ** ist, zahlen Sie jeden Monat aus eigener Tasche für das neue Haus, aber die Mieteinnahmen subventionieren es. Sie sollten diese Eigenbeteiligung mit Ihrer *Gewünschten monatlichen Rate* vergleichen, um zu sehen, ob sie Ihrem persönlichen Grenzwert entspricht.
        - Vergessen Sie nicht, dass Mieteinnahmen steuerpflichtig sind! Die hier gezeigten Einnahmen sind *Brutto*-Mieteinnahmen vor Einkommensteuer. Sie können jedoch auch die Abschreibung (AfA) auf das alte Haus absetzen, um diese Steuerlast zu senken.
        """)

        # Calculate affordability threshold
        max_affordable_payment = desired_monthly_payment + monthly_rent
        max_loan_capacity = npf.pv(monthly_interest_rate, total_months, -max_affordable_payment, 0)
        max_purchase_price = max_loan_capacity + down_payment - renovations_new
        # adjust for closing costs
        max_purchase_price = max_purchase_price / (1 + (closing_costs_percent / 100))

        st.subheader("Maximaler Erschwinglichkeits-Grenzwert")
        st.write(f"Basierend auf Ihrer gewünschten Eigenbeteiligung von **€{format_eur(desired_monthly_payment)}** und erwarteten Mieteinnahmen von **€{format_eur(monthly_rent)}**, können Sie sich eine monatliche Gesamthypothekenrate von **€{format_eur(max_affordable_payment)}** leisten.")
        st.write(f"Unter Annahme desselben Zinssatzes ({interest_rate}%), derselben Laufzeit ({duration_years} Jahre), desselben Eigenkapitals und derselben Renovierungskosten, beträgt der **maximale Kaufpreis**, den Sie für das neue Haus in Betracht ziehen sollten, etwa **€{format_eur(max_purchase_price)}**.")
