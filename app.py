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
button[aria-label="Step up"] {
    display: none !important;
}
button[aria-label="Step down"] {
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

st.write("Ermitteln Sie die finanzielle Machbarkeit des Kaufs eines neuen Hauses zur Eigennutzung, unabhängig davon, ob Sie Ihr aktuelles Haus vermieten oder verkaufen.")

def format_eur(amount):
    """Format numbers into German EUR style, e.g., 1.000,00"""
    import math
    if math.isinf(amount):
        return "∞"
    formatted = f"{amount:,.2f}"
    return formatted.replace(",", "X").replace(".", ",").replace("X", ".")


def berechne_netto(brutto_jahr, kv_satz):
    """
    Approximation of the monthly net salary for 2024 (Hesse, Tax Class 1, no church tax).
    """
    if brutto_jahr <= 0:
        return 0.0

    bbg_kv = 62100.0
    bbg_rv = 90600.0

    kv_anteil = kv_satz / 2.0 / 100.0
    pv_anteil = 0.023 # Steuerklasse 1 oft kinderlos = 2.3%
    rv_anteil = 0.093
    av_anteil = 0.013

    basis_kv = min(brutto_jahr, bbg_kv)
    basis_rv = min(brutto_jahr, bbg_rv)

    soz_kv_pv = basis_kv * (kv_anteil + pv_anteil)
    soz_rv_av = basis_rv * (rv_anteil + av_anteil)
    sozialabgaben = soz_kv_pv + soz_rv_av

    # Vorsorgeaufwendungen absetzen (stark vereinfacht)
    vorsorge = min(sozialabgaben, 1900 + soz_rv_av)
    zve = brutto_jahr - 1230.0 - vorsorge
    if zve < 0: zve = 0

    # ESt-Tarif 2024
    if zve <= 11784:
        est = 0.0
    elif zve <= 17005:
        y = (zve - 11784) / 10000.0
        est = (992.14 * y + 1400.0) * y
    elif zve <= 62809:
        z = (zve - 17005) / 10000.0
        est = (208.85 * z + 2397.0) * z + 966.53
    elif zve <= 277825:
        est = 0.42 * zve - 10453.18
    else:
        est = 0.45 * zve - 18787.93

    est = max(0, est)
    # Soli
    soli = 0.0
    if est > 18130:
        soli = est * 0.055

    netto_jahr = brutto_jahr - sozialabgaben - est - soli
    return netto_jahr / 12.0


tab_vermietung, tab_verkauf, tab_erklaerung = st.tabs(["Szenario Vermietung", "Szenario Verkauf", "Erklärung"])

with tab_vermietung:
    row1_col1, row1_col2 = st.columns(2)

    with row1_col2:
        with st.container(border=True):
            st.header("Das Alte Haus (Vermietung)")

            r4c1, r4c2, r4c3 = st.columns(3)
            with r4c1:
                monthly_rent = st.number_input("Monatliche Mieteinnahmen", value=1400, step=None)
            with r4c2:
                renovations_old = st.number_input("Reparaturen vor Vermietung", value=10000, step=None)
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
            st.header("Das Neue Haus (Kauf)")

            r1c1, r1c2, r1c3 = st.columns(3)
            with r1c1:
                purchase_price = st.number_input("Kaufpreis (€)", value=600000, step=None)
            with r1c2:
                closing_costs_percent = st.number_input("Kaufnebenkosten (%)", value=8.0, step=None, help="In Hessen beträgt die Grunderwerbsteuer 6%. Notar und Grundbuchamt machen ca. 2% aus.")
            with r1c3:
                renovations_new = st.number_input("Reparaturen vor Einzug", value=10000, step=None)

            r1a1, r1a2, r1a3 = st.columns(3)
            with r1a1:
                down_payment = st.number_input("Eigenkapital (€)", value=160000, step=None, help="Bargeld, das Sie für den Kauf, die Nebenkosten und Renovierungen einsetzen.")
            with r1a2:
                wohnflaeche_new = st.number_input("Wohnfläche (m²)", value=250, step=None)
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
                nk_haftpflicht_old = st.number_input("Haftpflicht 📌", value=100, step=None, key="nk_haft_old")
            with nko1c2:
                nk_versicherung_old = st.number_input("Wohngebäudevers. 📌", value=1100, step=None, key="nk_vers_old")
            with nko1c3:
                nk_grundsteuer_old = st.number_input("Grundsteuer 📌", value=430, step=None, key="nk_gs_old")
            with nko1c4:
                nk_muell_old = st.number_input("Müll/Straßenreinigung 📌", value=200, step=None, key="nk_muell_old")

            nko2c1, nko2c2, nko2c3, nko2c4 = st.columns(4)
            with nko2c1:
                nk_wasser_old = st.number_input("Wasser/Kanal/Niederschlag 📌", value=525, step=None, key="nk_wasser_old", help="Wasser, Kanalgebühren & Niederschlagswasser.")
            with nko2c2:
                nk_schornstein_old = st.number_input("Schornsteinfeger/Heizung 📌", value=300, step=None, key="nk_schorn_old")
            with nko2c3:
                nk_verbrauch_old = st.number_input("Verbrauchskosten 📌", value=4020, step=None, key="nk_verbr_old")
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
            st.write("Berechnung des Netto-Gehalts für Steuerklasse 1 in Hessen ohne Kirchensteuer.")
            r5c1, r5c2, r5c3 = st.columns(3)
            with r5c1:
                brutto_jahr = st.number_input("Jährliches Bruttogehalt (€)", value=55000, step=None)
            with r5c2:
                kv_satz = st.number_input("Gesetzlicher Krankenkassenbeitrag (%)", value=16.8, step=None, format="%.1f")
            with r5c3:
                other_income = st.number_input("Andere Einkommensquellen (Netto/Monat €)", value=0, step=None)

            job_salary_net = berechne_netto(brutto_jahr, kv_satz)

            st.markdown(f"**Berechnetes monatliches Netto-Gehalt:** €{format_eur(job_salary_net)}")

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
                priv_nahrung = st.number_input("Nahrungsmittel", value=200, step=None)
            with pr1c2:
                priv_mobilitaet = st.number_input("Mobilität (Auto, ÖPNV)", value=43.50, step=None)
            with pr1c3:
                priv_versicherungen = st.number_input("Versicherungen", value=150, step=None)

            pr2c1, pr2c2, pr2c3 = st.columns(3)
            with pr2c1:
                priv_kommunikation = st.number_input("Kommunikation (Handy, Internet)", value=60, step=None)
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
            help_svg = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="currentColor" xmlns="http://www.w3.org/2000/svg" color="inherit" style="width: 1rem; height: 1rem; margin-left: 4px; vertical-align: middle; color: rgba(49, 51, 63, 0.6);"><path fill="none" d="M0 0h24v24H0V0z"></path><path d="M11 18h2v-2h-2v2zm1-16C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm0-14c-2.21 0-4 1.79-4 4h2c0-1.1.9-2 2-2s2 .9 2 2c0 2-3 1.75-3 5h2c0-2.25 3-2.5 3-5 0-2.21-1.79-4-4-4z"></path></svg>'

            with b1:
                st.markdown(f"**Beleihungsauslauf (LTV)** <span title='Zeigt, wie viel Prozent des eigentlichen Hauswertes die Bank finanzieren muss. Unter 80 % ist gut, unter 60 % gibt es Bestzinsen.' style='cursor: help;'>{help_svg}</span><br><span style='color:{ltv_color}; font-weight:bold;'>{format_eur(ltv_pct)} %</span>", unsafe_allow_html=True)
                st.markdown(f"**Wohnkostenquote** <span title='Prüft, wie viel Prozent unseres monatlichen Haushaltsnettoeinkommens für die Rate draufgehen. Das darf für die Bank nicht über 40 % rutschen.' style='cursor: help;'>{help_svg}</span><br><span style='color:{wkq_color}; font-weight:bold;'>{format_eur(wkq_pct)} %</span>", unsafe_allow_html=True)
            with b2:
                st.markdown(f"**Bewirtschaftungspauschale** <span title='Das ist der Puffer, den die Bank in ihrer Haushaltsrechnung für Heizung, Instandhaltung und Müll abzieht. Sie rechnet meist mit 2,50 € pro Quadratmeter im Monat.' style='cursor: help;'>{help_svg}</span><br>€{format_eur(bewirtschaftung_pauschale)}", unsafe_allow_html=True)
                st.markdown(f"**1. Monat Zins / Tilgung** <span title='Damit wir direkt sehen, wie viel von unserer hohen Rate im ersten Monat in den eigenen Vermögensaufbau (Tilgung) und wie viel an die Bank (Zins) fließt.' style='cursor: help;'>{help_svg}</span><br>€{format_eur(zins_anteil_1m)} / €{format_eur(tilgung_anteil_1m)}", unsafe_allow_html=True)

        st.markdown("<div style='margin-bottom: 30px;'></div>", unsafe_allow_html=True)

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

                # Scenario A
                net_monthly_cash_flow_a = total_monthly_income + net_rental_surplus - total_monthly_burden
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

                # Scenario B: empty house means no rent, owner pays old house Nebenkosten
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



with tab_verkauf:
    row1_vk1, row1_vk2 = st.columns(2)

    with row1_vk1:
        with st.container(border=True):
            st.header("Das Neue Haus (Kauf)")

            r1c1, r1c2, r1c3 = st.columns(3)
            with r1c1:
                vk_purchase_price = st.number_input("Kaufpreis (€)", value=600000, step=None, key="vk_purchase")
            with r1c2:
                vk_closing_costs_percent = st.number_input("Kaufnebenkosten (%)", value=8.0, step=None, help="In Hessen beträgt die Grunderwerbsteuer 6%. Notar und Grundbuchamt machen ca. 2% aus.", key="vk_closing")
            with r1c3:
                vk_renovations_new = st.number_input("Reparaturen & Umzug (€)", value=20000, step=None, key="vk_renov")

            r1a1, r1a2, r1a3 = st.columns(3)
            with r1a1:
                vk_down_payment = st.number_input("Netto-Erlös Verkauf Altes Haus (€)", value=300000, step=None, help="Konservativ geschätzt", key="vk_netto_erloes")
            with r1a2:
                vk_sonstiges_eigenkapital = st.number_input("Sonstiges Eigenkapital (€)", value=160000, step=None, help="Ersparnisse etc.", key="vk_sonstiges_ek")
            with r1a3:
                vk_wohnflaeche_new = st.number_input("Wohnfläche (m²)", value=250, step=None, key="vk_wohn")

            vk_closing_costs_eur = vk_purchase_price * (vk_closing_costs_percent / 100)
            vk_total_capital_needed = vk_purchase_price + vk_closing_costs_eur + vk_renovations_new
            vk_gesamtes_eigenkapital = vk_down_payment + vk_sonstiges_eigenkapital
            vk_loan_amount = max(0, vk_total_capital_needed - vk_gesamtes_eigenkapital)

            r2c1, r2c2, r2c3, r2c4 = st.columns(4)
            with r2c1:
                st.markdown(f'<div class="calculated-result" style="margin-top: 10px;">Benötigtes Kapital: <b>€{format_eur(vk_total_capital_needed)}</b></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="calculated-result">Gesamtes Eigenkapital: <b>€{format_eur(vk_gesamtes_eigenkapital)}</b></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="calculated-result">Benötigter Kreditbetrag: <b>€{format_eur(vk_loan_amount)}</b></div>', unsafe_allow_html=True)
            with r2c2:
                st.markdown(f'<div class="calculated-result" style="margin-top: 10px;">Kaufnebenkosten: <b>€{format_eur(vk_closing_costs_eur)}</b></div>', unsafe_allow_html=True)
            with r2c3:
                pass
            with r2c4:
                pass

    with row1_vk2:
        with st.container(border=True):
            st.header("Hypotheken-Details")
            h4c1, h4c2, h4c3, h4c4 = st.columns(4)
            with h4c1:
                vk_interest_rate = st.number_input("Zinssatz (%)", value=3.5, step=None, key="vk_int")
            with h4c2:
                vk_tilgungssatz = st.number_input("Anfängl. Tilgung (%)", value=2.0, step=None, key="vk_tilg")
            with h4c3:
                vk_zinsbindung = st.number_input("Zinsbindung (Jahre)", value=15, step=None, key="vk_bind")
            with h4c4:
                vk_sondertilgung = st.number_input("Jährl. Sondertilgung (€)", value=0, step=None, key="vk_sond")

            vk_monthly_interest_rate = (vk_interest_rate / 100) / 12

            if vk_loan_amount > 0:
                vk_actual_monthly_payment = (vk_loan_amount * ((vk_interest_rate + vk_tilgungssatz) / 100)) / 12

                # Simulated calculation
                balance = vk_loan_amount
                months = 0
                restschuld_nach_bindung = 0

                if vk_actual_monthly_payment <= (vk_loan_amount * vk_monthly_interest_rate) and vk_sondertilgung == 0:
                    months = float("inf")
                    restschuld_nach_bindung = float("inf")
                else:
                    while balance > 0 and months < 1200: # 100 years max
                        interest_payment = balance * vk_monthly_interest_rate
                        principal_payment = vk_actual_monthly_payment - interest_payment
                        balance -= principal_payment
                        months += 1

                        if months % 12 == 0:
                            balance -= vk_sondertilgung

                        if balance < 0:
                            balance = 0

                        if months == (vk_zinsbindung * 12):
                            restschuld_nach_bindung = balance

                vk_years = months // 12
                vk_remaining_months = months % 12

                if months >= 1200 or months == float("inf"):
                    time_str = "∞"
                else:
                    time_str = f"{int(vk_years)} Jahre, {int(vk_remaining_months)} Monate"
            else:
                vk_actual_monthly_payment = 0.0
                time_str = "0 Jahre, 0 Monate"
                restschuld_nach_bindung = 0.0

            st.markdown(f'<div class="calculated-result" style="margin-top: 10px; font-size: 1.2rem;">Monatliche Rate: <b>€{format_eur(vk_actual_monthly_payment)}</b></div>', unsafe_allow_html=True)

            h5c1, h5c2, h5c3 = st.columns(3)
            with h5c1:
                st.markdown(f'<div class="calculated-result" style="margin-top: 10px;">Gesamtlaufzeit: <b>{time_str}</b></div>', unsafe_allow_html=True)
            with h5c2:
                st.markdown(f'<div class="calculated-result" style="margin-top: 10px;">Restschuld nach {vk_zinsbindung} Jahren: <b>€{format_eur(restschuld_nach_bindung)}</b></div>', unsafe_allow_html=True)
            with h5c3:
                pass

    # --- ROW 2: Laufende Nebenkosten & Einkommen ---
    row2_vk1, row2_vk2 = st.columns(2)

    with row2_vk1:
        with st.container(border=True):
            st.header("Laufende Nebenkosten (Jahr)")

            nk1c1, nk1c2, nk1c3, nk1c4 = st.columns(4)
            with nk1c1:
                vk_nk_versicherung_new = st.number_input("Wohngebäudevers.", value=1000, step=None, key="vk_nk_vers_new")
            with nk1c2:
                vk_nk_grundsteuer_new = st.number_input("Grundsteuer", value=550, step=None, key="vk_nk_gs_new")
            with nk1c3:
                vk_nk_muell_new = st.number_input("Müll/Straßenreinigung", value=200, step=None, key="vk_nk_muell_new")
            with nk1c4:
                vk_nk_wasser_new = st.number_input("Wasser/Kanal/Niederschlag", value=525, step=None, key="vk_nk_wasser_new", help="Wasser, Kanalgebühren & Niederschlagswasser")

            nk2c1, nk2c2, nk2c3, nk2c4 = st.columns(4)
            with nk2c1:
                vk_nk_schornstein_new = st.number_input("Schornsteinfeger/Heizung", value=300, step=None, key="vk_nk_schorn_new")
            with nk2c2:
                vk_nk_verbrauch_new = st.number_input("Verbrauchskosten", value=4020, step=None, key="vk_nk_verbr_new")
            with nk2c3:
                pass
            with nk2c4:
                pass

            vk_yearly_nebenkosten_new = vk_nk_versicherung_new + vk_nk_grundsteuer_new + vk_nk_muell_new + vk_nk_wasser_new + vk_nk_schornstein_new + vk_nk_verbrauch_new
            vk_monthly_nebenkosten_new = vk_yearly_nebenkosten_new / 12

            nk3c1, nk3c2, nk3c3, nk3c4 = st.columns(4)
            with nk3c1:
                st.markdown(f'<div class="calculated-result">Jährliche Nebenkosten: <b>€{format_eur(vk_yearly_nebenkosten_new)}</b></div>', unsafe_allow_html=True)
            with nk3c2:
                st.markdown(f'<div class="calculated-result">Monatliche Nebenkosten: <b>€{format_eur(vk_monthly_nebenkosten_new)}</b></div>', unsafe_allow_html=True)
            with nk3c3:
                pass
            with nk3c4:
                pass

    with row2_vk2:
        with st.container(border=True):
            st.header("Einkommen")
            st.write("Berechnung des Netto-Gehalts für Steuerklasse 1 in Hessen ohne Kirchensteuer.")
            r5c1, r5c2, r5c3 = st.columns(3)
            with r5c1:
                vk_brutto_jahr = st.number_input("Jährliches Bruttogehalt (€)", value=55000, step=None, key="vk_brutto")
            with r5c2:
                vk_kv_satz = st.number_input("Gesetzlicher Krankenkassenbeitrag (%)", value=16.8, step=None, format="%.1f", key="vk_kv")
            with r5c3:
                vk_other_income = st.number_input("Andere Einkommensquellen (Netto/Monat €)", value=0, step=None, key="vk_other")

            vk_job_salary_net = berechne_netto(vk_brutto_jahr, vk_kv_satz)

            st.markdown(f"**Berechnetes monatliches Netto-Gehalt:** €{format_eur(vk_job_salary_net)}")

            vk_total_monthly_income = vk_job_salary_net + vk_other_income

    # --- ROW 3: Privatkosten & Finanzielle Analyse ---
    row3_vk1, row3_vk2 = st.columns(2)

    with row3_vk1:
        with st.container(border=True):
            st.header("Laufende Kosten (Privat, mtl.)")
            pr1c1, pr1c2, pr1c3 = st.columns(3)
            with pr1c1:
                vk_priv_nahrung = st.number_input("Nahrungsmittel", value=200, step=None, key="vk_priv_nahr")
            with pr1c2:
                vk_priv_mobilitaet = st.number_input("Mobilität (Auto, ÖPNV)", value=43.50, step=None, key="vk_priv_mob")
            with pr1c3:
                vk_priv_versicherungen = st.number_input("Versicherungen", value=150, step=None, key="vk_priv_vers")

            pr2c1, pr2c2, pr2c3 = st.columns(3)
            with pr2c1:
                vk_priv_kommunikation = st.number_input("Kommunikation (Handy, Internet)", value=60, step=None, key="vk_priv_kom")
            with pr2c2:
                vk_priv_sonstiges = st.number_input("Sonstiges", value=100, step=None, key="vk_priv_son")
            with pr2c3:
                pass

            vk_monthly_nebenkosten_privat = vk_priv_nahrung + vk_priv_mobilitaet + vk_priv_versicherungen + vk_priv_kommunikation + vk_priv_sonstiges

            pr3c1, pr3c2, pr3c3 = st.columns(3)
            with pr3c1:
                st.markdown(f'<div class="calculated-result" style="margin-top: 10px;">Jährliche Privatkosten: <b>€{format_eur(vk_monthly_nebenkosten_privat * 12)}</b></div>', unsafe_allow_html=True)
            with pr3c2:
                st.markdown(f'<div class="calculated-result" style="margin-top: 10px;">Monatliche Privatkosten: <b>€{format_eur(vk_monthly_nebenkosten_privat)}</b></div>', unsafe_allow_html=True)
            with pr3c3:
                pass

        with st.container(border=True):
            st.header("Bank-Risikoprüfung 🏦")

            # 1. Beleihungsauslauf (LTV)
            vk_ltv = vk_loan_amount / vk_purchase_price if vk_purchase_price > 0 else 0
            vk_ltv_pct = vk_ltv * 100
            vk_ltv_color = "green" if vk_ltv_pct < 60 else "orange" if vk_ltv_pct <= 80 else "red"

            # 2. Wohnkostenquote (Kapitaldienstgrenze)
            vk_wkq = vk_actual_monthly_payment / vk_total_monthly_income if vk_total_monthly_income > 0 else 0
            vk_wkq_pct = vk_wkq * 100
            vk_wkq_color = "green" if vk_wkq_pct <= 30 else "orange" if vk_wkq_pct <= 40 else "red"

            # 3. Bewirtschaftungspauschale
            vk_bewirtschaftung_pauschale = vk_wohnflaeche_new * 2.5

            # 4. Zins- und Tilgungsanteil (für den 1. Monat)
            vk_zins_anteil_1m = vk_loan_amount * (vk_interest_rate / 100 / 12)
            vk_tilgung_anteil_1m = vk_actual_monthly_payment - vk_zins_anteil_1m

            b1, b2 = st.columns(2)
            help_svg = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="currentColor" xmlns="http://www.w3.org/2000/svg" color="inherit" style="width: 1rem; height: 1rem; margin-left: 4px; vertical-align: middle; color: rgba(49, 51, 63, 0.6);"><path fill="none" d="M0 0h24v24H0V0z"></path><path d="M11 18h2v-2h-2v2zm1-16C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm0-14c-2.21 0-4 1.79-4 4h2c0-1.1.9-2 2-2s2 .9 2 2c0 2-3 1.75-3 5h2c0-2.25 3-2.5 3-5 0-2.21-1.79-4-4-4z"></path></svg>'

            with b1:
                st.markdown(f"**Beleihungsauslauf (LTV)** <span title='Zeigt, wie viel Prozent des eigentlichen Hauswertes die Bank finanzieren muss. Unter 80 % ist gut, unter 60 % gibt es Bestzinsen.' style='cursor: help;'>{help_svg}</span><br><span style='color:{vk_ltv_color}; font-weight:bold;'>{format_eur(vk_ltv_pct)} %</span>", unsafe_allow_html=True)
                st.markdown(f"**Wohnkostenquote** <span title='Prüft, wie viel Prozent unseres monatlichen Haushaltsnettoeinkommens für die Rate draufgehen. Das darf für die Bank nicht über 40 % rutschen.' style='cursor: help;'>{help_svg}</span><br><span style='color:{vk_wkq_color}; font-weight:bold;'>{format_eur(vk_wkq_pct)} %</span>", unsafe_allow_html=True)
            with b2:
                st.markdown(f"**Bewirtschaftungspauschale** <span title='Das ist der Puffer, den die Bank in ihrer Haushaltsrechnung für Heizung, Instandhaltung und Müll abzieht. Sie rechnet meist mit 2,50 € pro Quadratmeter im Monat.' style='cursor: help;'>{help_svg}</span><br>€{format_eur(vk_bewirtschaftung_pauschale)}", unsafe_allow_html=True)
                st.markdown(f"**1. Monat Zins / Tilgung** <span title='Damit wir direkt sehen, wie viel von unserer hohen Rate im ersten Monat in den eigenen Vermögensaufbau (Tilgung) und wie viel an die Bank (Zins) fließt.' style='cursor: help;'>{help_svg}</span><br>€{format_eur(vk_zins_anteil_1m)} / €{format_eur(vk_tilgung_anteil_1m)}", unsafe_allow_html=True)

    with row3_vk2:
        with st.container(border=True):
            st.header("Finanzielle Analyse 💰")

            vk_total_monthly_burden = vk_actual_monthly_payment + vk_monthly_nebenkosten_new + vk_monthly_nebenkosten_privat

            st.subheader("Ausgaben (Monatlich)")

            ausg1, ausg2, ausg3 = st.columns(3)
            with ausg1:
                st.metric("Erforderliche Rate (Kredit)", f"€{format_eur(vk_actual_monthly_payment)}")
            with ausg2:
                st.metric("Nebenkosten (Haus)", f"€{format_eur(vk_monthly_nebenkosten_new)}")
            with ausg3:
                st.metric("Privatkosten", f"€{format_eur(vk_monthly_nebenkosten_privat)}")

            st.markdown(f'<div class="calculated-result" style="margin-top:15px; font-size: 1.5rem;">Gesamte monatliche Belastung: <b>€{format_eur(vk_total_monthly_burden)}</b></div>', unsafe_allow_html=True)

            st.markdown("---")
            st.write("Vergleich der monatlichen Ausgaben mit Ihrem Einkommen.")

            st.subheader("Szenario Verkauf")

            vk_net_monthly_cash_flow = vk_total_monthly_income - vk_total_monthly_burden
            vk_net_yearly_cash_flow = vk_net_monthly_cash_flow * 12

            box_class = "cashflow-positive" if vk_net_monthly_cash_flow >= 0 else "cashflow-negative"
            st.markdown(f"""
            <div class="cashflow-box {box_class}">
                <div class="cashflow-label">Netto Cashflow (Frei verfügbarer Puffer)</div>
                <div class="cashflow-value">€{format_eur(vk_net_monthly_cash_flow)}</div>
            </div>
            """, unsafe_allow_html=True)
            st.write(f"**Jährlicher Netto Cashflow:** €{format_eur(vk_net_yearly_cash_flow)}")

with tab_erklaerung:
    st.header("📖 Funktionsweise & Berechnungen")
    st.markdown("Diese Seite erklärt detailliert, wie der Hausprojekt-Rechner funktioniert, welche Annahmen getroffen werden und wie sich die Endergebnisse zusammensetzen.")

    st.markdown("---")
    st.subheader("Szenario Vermietung")
    st.markdown("""
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

### 4. Einkommen & Privatkosten
Damit der Cashflow realistisch ist, betrachten wir Ihr verfügbares Budget:
- **Netto-Gehalt:** Das monatliche Netto-Gehalt wird basierend auf Ihrem jährlichen Bruttogehalt und dem gesetzlichen Krankenkassenbeitrag automatisch geschätzt (Annahme: Bundesland Hessen, Steuerklasse 1, keine Kirchensteuer).
- Dieses Netto-Gehalt sowie **weitere Einkommensquellen** bilden die Einnahmenseite.
- Davon abgezogen werden die **Laufenden Kosten (Privat)** wie Nahrungsmittel, Versicherungen und Sonstiges.

### 5. Finanzielle Analyse (Szenarien)
Die abschließende Analyse führt alle Ausgaben und Einnahmen zusammen, um Ihren finalen Netto-Cashflow zu ermitteln.

Die **Gesamte monatliche Belastung** setzt sich zusammen aus der Kreditrate für das neue Haus, den Nebenkosten des neuen Hauses und Ihren privaten Lebenshaltungskosten.

* **Szenario A (Vermietet):**
  Ihr Einkommen wird um den *Netto-Mietüberschuss (nach Steuern)* ergänzt. Davon ziehen wir die gesamte monatliche Belastung ab.

* **Szenario B (Leerstand):**
  Das alte Haus bringt keine Mieteinnahmen. Ihr Einkommen muss nun die gesamte monatliche Belastung **sowie zusätzlich** die vollen monatlichen Nebenkosten des leerstehenden alten Hauses tragen.

Sollte der Cashflow-Wert rot sein, übersteigen Ihre monatlichen Ausgaben Ihre Einnahmen.

### 6. Bank-Risikoprüfung
Hier sehen Sie die wichtigsten Kennzahlen, die Banken intern zur Kreditvergabe nutzen:
- **Beleihungsauslauf (LTV):** Prozentualer Anteil des Kaufpreises, der finanziert wird. (< 60% = Bestzinsen, > 80% = Risiko).
- **Wohnkostenquote:** Zeigt, wie viel Prozent Ihres Nettoeinkommens für die monatliche Kreditrate aufgewendet werden muss. (Sollte unter 30-40% liegen).
- **Bewirtschaftungspauschale:** Pauschaler Abzug der Bank für Nebenkosten (oft 2,50 € pro m²).
- **Zins- und Tilgungsanteil (1. Monat):** Zeigt auf einen Blick, wie viel Ihrer ersten Rate in Ihren Vermögensaufbau (Tilgung) und wie viel an die Bank (Zinsen) fließt.
    """)

    st.markdown("---")
    st.subheader("Szenario Verkauf")
    st.markdown("""
Im Reiter **Szenario Verkauf** vergleichen wir die Option, das alte Haus nicht zu vermieten, sondern abzustoßen, um den Erlös als Eigenkapital für das neue Haus zu nutzen.
* **1. Kapitalbedarf:** Bündelt Kaufpreis, Nebenkosten und Reparaturen & Umzug des neuen Hauses.
* **2. Eigenkapital:** Setzt sich aus dem erwarteten Netto-Erlös Ihres alten Hauses sowie weiteren Ersparnissen zusammen.
* **3. Kreditkosten:** Da das Eigenkapital deutlich höher ist, fällt die benötigte Kreditsumme geringer aus. Die Rate wird klassisch mit Zinssatz und Tilgung berechnet. Hier sehen Sie auch die verbleibende Restschuld am Ende der Zinsbindung.
* **4. Haushaltsrechnung:** Prüft, ob Ihr Haushaltsnettoeinkommen (basierend auf Ihrem Bruttogehalt) ausreicht, um die neue Kreditrate, die kalkulatorische Bewirtschaftung des neuen Hauses (2,50 € pro m²) und Ihre regulären Lebenshaltungskosten zu decken.
* **5. Bank-Risikoprüfung:** Zeigt LTV, Wohnkostenquote und den exakten Tilgungs-/Zinsanteil der Rate im ersten Monat nach finanzmathematischen Standards.
    """)
