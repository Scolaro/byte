import streamlit as st
import numpy_financial as npf

st.set_page_config(page_title="House Project Calculator", layout="wide")

st.title("🏡 House Project Calculator (Hesse, Germany)")
st.write("Determine the financial viability of buying a new house to live in, while renting out your current house.")

# Layout
col1, col2 = st.columns(2)

with col1:
    st.header("1. The New House")

    st.subheader("Purchase & Initial Costs")
    purchase_price = st.number_input("Purchase Price (€)", value=400000, step=10000)

    st.write("**Closing Costs (Kaufnebenkosten)**")
    # Grunderwerbsteuer in Hesse is 6%, Notary ~2% -> Let's default to 8% total without Makler
    closing_costs_percent = st.number_input("Closing Costs (%)", value=8.0, step=0.1, help="In Hesse, property transfer tax is 6%. Notary and land registry are approx 2%.")
    closing_costs_eur = purchase_price * (closing_costs_percent / 100)
    st.write(f"Calculated Closing Costs: **€{closing_costs_eur:,.2f}**")

    renovations_new = st.number_input("Estimated Repairs/Renovations for New House (€)", value=50000, step=5000)
    down_payment = st.number_input("Down Payment / Eigenkapital (€)", value=100000, step=5000, help="Amount of cash you are putting towards the purchase, closing costs, and renovations.")

    total_capital_needed = purchase_price + closing_costs_eur + renovations_new
    loan_amount = total_capital_needed - down_payment

    st.write(f"Total Capital Needed: **€{total_capital_needed:,.2f}**")
    st.write(f"Required Mortgage Amount: **€{loan_amount:,.2f}**")

    st.subheader("Mortgage Details")
    interest_rate = st.number_input("Mortgage Interest Rate (%)", value=3.5, step=0.1)
    duration_years = st.number_input("Duration of Mortgage (Years)", value=25, step=1)
    desired_monthly_payment = st.number_input("Desired Monthly Mortgage Payment (€)", value=1500, step=100)


with col2:
    st.header("2. The Old House (Rental)")

    st.subheader("Rental Income")
    monthly_rent = st.number_input("Desired Monthly Rent Income (Kaltmiete) (€)", value=1200, step=50)

    st.subheader("Renovations & Tax Deductions")
    renovations_old = st.number_input("Repairs/Renovations before renting out (€)", value=20000, step=1000)
    marginal_tax_rate = st.slider("Your Marginal Tax Rate (Grenzsteuersatz) (%)", min_value=15, max_value=45, value=42, step=1, help="Used to calculate your tax savings. In Germany, highest income tax rate is 42% (or 45% for very high income).")


st.markdown("---")
st.header("3. Financial Analysis & Threshold")
# Calculations for New House Mortgage
if loan_amount <= 0:
    st.success("Your down payment covers all costs! No mortgage needed.")
else:
    # Monthly interest rate
    monthly_interest_rate = (interest_rate / 100) / 12
    total_months = duration_years * 12

    # Calculate the required monthly payment to zero out the loan
    actual_monthly_payment = -npf.pmt(monthly_interest_rate, total_months, loan_amount)

    st.subheader("New House Costs")

    col3, col4 = st.columns(2)
    with col3:
        st.metric("Actual Required Monthly Payment", f"€{actual_monthly_payment:,.2f}")
    with col4:
        st.metric("Desired Monthly Payment", f"€{desired_monthly_payment:,.2f}")

    deficit = actual_monthly_payment - desired_monthly_payment

    if deficit > 0:
        st.error(f"⚠️ **Deficit Detected**: The required payment is €{deficit:,.2f} higher than your desired payment each month.")

        # Calculate Yearly Single Payment (Sondertilgung)
        # We need to find how much extra lump sum needs to be paid per year to make up for the lower monthly payment
        # If paying desired_monthly_payment, what is the remaining balance at the end of each year?
        # A simpler way to express this:
        # The deficit happens 12 times a year. A yearly payment to offset this isn't exactly deficit * 12 due to interest,
        # but paying a yearly Sondertilgung to bridge the gap means we calculate the future value of the deficit over a year, or
        # basically we need to inject enough capital yearly to keep the amortization schedule on track.

        yearly_sondertilgung = deficit * 12
        # To be completely mathematically accurate on the loan schedule, the bank essentially requires you to pay the deficit.
        # Paying it at the end of the year requires slightly more due to interest accrued on the deficit.
        # FV of the monthly deficit over 12 months:
        yearly_sondertilgung_with_interest = npf.fv(monthly_interest_rate, 12, -deficit, 0)

        st.warning(f"💡 To keep your monthly payments at **€{desired_monthly_payment:,.2f}** and still pay off the loan in **{duration_years} years**, you would need to make a single extra yearly payment (Sondertilgung) of approximately **€{yearly_sondertilgung_with_interest:,.2f}**.")
    else:
        surplus = desired_monthly_payment - actual_monthly_payment
        st.success(f"✅ **Threshold Met**: Your desired payment is sufficient! You have a surplus of €{surplus:,.2f} per month.")


st.markdown("---")
st.subheader("Old House (Rental) Financials")

yearly_rent = monthly_rent * 12
st.write(f"Yearly Rent Income (Kaltmiete): **€{yearly_rent:,.2f}**")

# Tax Deductions
tax_savings = renovations_old * (marginal_tax_rate / 100)
net_renovation_cost = renovations_old - tax_savings

st.write(f"Estimated Tax Savings from Renovations: **€{tax_savings:,.2f}**")
st.write(f"Net Cost of Renovations (After Tax): **€{net_renovation_cost:,.2f}**")

with st.expander("ℹ️ How do tax deductions for the old house work in Germany?"):
    st.write(f"""
    In Germany, if you rent out a property, costs incurred to maintain or repair the property (Erhaltungsaufwand) can be deducted from your rental income as *Werbungskosten*.

    Since your marginal tax rate is set to **{marginal_tax_rate}%**, for every €1,000 you spend on repairs, you reduce your taxable income by €1,000, effectively saving you €{(1000 * marginal_tax_rate/100):.2f} in taxes.

    *Note: If the renovation costs exceed 15% of the building's value within the first 3 years of purchasing (anschaffungsnaher Herstellungsaufwand), they must be depreciated over 50 years at 2% per year. However, since you already own this house and lived in it, immediate deduction is usually applicable for maintenance and repairs.*
    """)

st.markdown("---")
st.header("4. Overall Cash Flow Summary")
st.write("Combining the costs of the new house with the income from the old house.")

if loan_amount > 0:
    net_monthly_cash_flow = monthly_rent - actual_monthly_payment
    net_yearly_cash_flow = (monthly_rent * 12) - (actual_monthly_payment * 12)

    st.subheader("Monthly Overview")
    col5, col6, col7 = st.columns(3)
    col5.metric("Rental Income", f"+ €{monthly_rent:,.2f}")
    col6.metric("Mortgage Payment", f"- €{actual_monthly_payment:,.2f}")
    col7.metric("Net Monthly Cash Flow", f"€{net_monthly_cash_flow:,.2f}",
                delta_color="normal" if net_monthly_cash_flow >= 0 else "inverse",
                delta=f"€{net_monthly_cash_flow:,.2f}")

    st.write(f"**Yearly Net Cash Flow:** €{net_yearly_cash_flow:,.2f}")

    st.info("""
    **Understanding the Outcome:**
    - If your net monthly cash flow is **positive**, your rental income covers your entire new mortgage.
    - If your net monthly cash flow is **negative**, you are paying out of pocket each month for the new house, but the rental income is subsidizing it. You should compare this out-of-pocket expense against your *Desired Monthly Payment* to see if it meets your personal threshold.
    - Don't forget that rental income is taxable! The income shown here is *gross* rental income before income tax. However, you can also deduct depreciation (AfA) on the old house to lower that tax burden.
    """)

    # Calculate affordability threshold
    max_affordable_payment = desired_monthly_payment + monthly_rent
    max_loan_capacity = npf.pv(monthly_interest_rate, total_months, -max_affordable_payment, 0)
    max_purchase_price = max_loan_capacity + down_payment - renovations_new
    # adjust for closing costs
    max_purchase_price = max_purchase_price / (1 + (closing_costs_percent / 100))

    st.subheader("Maximum Affordability Threshold")
    st.write(f"Based on your desired out-of-pocket payment of **€{desired_monthly_payment:,.2f}** and an expected rental income of **€{monthly_rent:,.2f}**, you can afford a total monthly mortgage payment of **€{max_affordable_payment:,.2f}**.")
    st.write(f"Assuming the same interest rate ({interest_rate}%), duration ({duration_years} years), down payment, and renovation costs, the **maximum purchase price** you should consider for the new house is roughly **€{max_purchase_price:,.2f}**.")
