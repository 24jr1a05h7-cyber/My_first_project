import streamlit as st
import requests


# Page configuration
st.set_page_config(
    page_title=" Jayanth's Currency Converter",
    page_icon="💱",
    layout="centered"
)


# Currency list
currencies = {
    "USD": "US Dollar",
    "INR": "Indian Rupee",
    "EUR": "Euro",
    "GBP": "British Pound",
    "JPY": "Japanese Yen",
    "AUD": "Australian Dollar",
    "CAD": "Canadian Dollar",
    "SGD": "Singapore Dollar",
    "AED": "UAE Dirham"
}


# Currency symbols
symbols = {
    "USD": "$",
    "INR": "₹",
    "EUR": "€",
    "GBP": "£",
    "JPY": "¥",
    "AUD": "A$",
    "CAD": "C$",
    "SGD": "S$",
    "AED": "د.إ"
}


# Initialize session state
if "from_currency" not in st.session_state:
    st.session_state.from_currency = "USD"

if "to_currency" not in st.session_state:
    st.session_state.to_currency = "INR"


# Swap currencies
def swap_currencies():
    old_from = st.session_state.from_currency
    old_to = st.session_state.to_currency

    st.session_state.from_currency = old_to
    st.session_state.to_currency = old_from


# Get exchange rate
def get_exchange_rate(from_currency, to_currency):
    url = (
        f"https://api.frankfurter.dev/v2/rate/"
        f"{from_currency}/{to_currency}"
    )

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    data = response.json()

    if "rate" not in data:
        raise ValueError("Exchange rate was not found.")

    return data["rate"], data.get("date")


# Application title
st.title("Jayanth's Currency Converter")

st.write(
    "Convert currencies easily using the latest available "
    "exchange rates from an online currency API."
)

st.divider()


# Currency selection
st.subheader("Select Currencies")

col1, col2 = st.columns(2)

with col1:
    st.selectbox(
        "From Currency",
        options=list(currencies.keys()),
        format_func=lambda code: f"{code} - {currencies[code]}",
        key="from_currency"
    )

with col2:
    st.selectbox(
        "To Currency",
        options=list(currencies.keys()),
        format_func=lambda code: f"{code} - {currencies[code]}",
        key="to_currency"
    )


# Swap button
st.button(
    "🔄 Swap Currencies",
    on_click=swap_currencies
)


# Amount input
st.subheader("Enter Amount")

amount = st.number_input(
    "Amount",
    min_value=0.01,
    value=100.00,
    step=1.00,
    format="%.2f"
)


# Convert button
if st.button("💱 Convert", use_container_width=True):

    from_currency = st.session_state.from_currency
    to_currency = st.session_state.to_currency

    # Validate currencies
    if from_currency == to_currency:
        st.warning(
            "⚠️ Please select two different currencies."
        )

    elif amount <= 0:
        st.warning(
            "⚠️ Please enter an amount greater than zero."
        )

    else:

        # Show loading message
        with st.spinner("🔄 Fetching latest exchange rate..."):

            try:
                rate, rate_date = get_exchange_rate(
                    from_currency,
                    to_currency
                )

                converted_amount = amount * rate

                st.success("Conversion successful!")

                st.divider()

                # Result section
                st.subheader("📊 Conversion Result")

                st.metric(
                    label="Converted Amount",
                    value=(
                        f"{symbols[to_currency]}"
                        f"{converted_amount:,.2f} "
                        f"{to_currency}"
                    )
                )

                st.write(
                    f"💵 **Amount:** "
                    f"{symbols[from_currency]}"
                    f"{amount:,.2f} {from_currency}"
                )

                st.write(
                    f"💱 **Exchange Rate:** "
                    f"1 {from_currency} = "
                    f"{rate:.6f} {to_currency}"
                )

                if rate_date:
                    st.write(
                        f"📅 **Rate Date:** {rate_date}"
                    )

            except requests.exceptions.Timeout:
                st.error(
                    "⚠️ The request timed out. "
                    "Please try again."
                )

            except requests.exceptions.ConnectionError:
                st.error(
                    "⚠️ Unable to connect to the currency API. "
                    "Please check your internet connection."
                )

            except requests.exceptions.HTTPError:
                st.error(
                    "⚠️ Unable to fetch the exchange rate. "
                    "Please check the selected currencies and try again."
                )

            except requests.exceptions.RequestException:
                st.error(
                    "⚠️ A network error occurred. "
                    "Please try again."
                )

            except (ValueError, KeyError):
                st.error(
                    "⚠️ Invalid exchange-rate data was received."
                )

            except Exception:
                st.error(
                    "⚠️ Something went wrong. "
                    "Please try again later."
                )


# Information section
st.divider()

st.subheader("ℹ️ About Currency Converter")

st.write(
    "This application uses the Frankfurter Exchange Rates API "
    "to obtain exchange-rate data and calculate currency conversions."
)

st.info(
    "Exchange rates can change over time. "
    "The displayed rate comes from the API and may represent "
    "the latest available working-day rate."
)


# Formula
st.subheader("🧮 Conversion Formula")

st.code(
    "Converted Amount = Amount × Exchange Rate"
)

st.write(
    "Example: If 1 USD = 83 INR, then:"
)

st.code(
    "100 USD × 83 = 8300 INR"
)