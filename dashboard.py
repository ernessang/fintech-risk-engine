import streamlit as st
import requests

st.set_page_config(page_title="Fintech Risk Dashboard", layout="wide")

st.title("💳 Fintech Risk Dashboard")

# INPUT
st.subheader("🧾 Nueva transacción")

amount = st.number_input("Monto", min_value=0.0, value=100.0)
country = st.text_input("País", value="MX")
merchant = st.text_input("Comercio", value="AMAZON")
tokenized = st.checkbox("¿Tokenizada?", value=True)

# BOTÓN
if st.button("Analizar transacción"):

    tx = {
        "amount": amount,
        "country": country,
        "merchant": merchant,
        "tokenized": tokenized,
        "ip": "8.8.8.8"  # puedes cambiar después
    }

    try:
        response = requests.post(
            "http://127.0.0.1:8000/analyze-transaction",
            json=tx,
            timeout=5
        )

        if response.status_code == 200:
            result = response.json()

            st.subheader("📊 Resultado")

            if result["decision"] == "APPROVE":
                st.success(f"Decision: {result['decision']}")
            elif result["decision"] == "REVIEW":
                st.warning(f"Decision: {result['decision']}")
            else:
                st.error(f"Decision: {result['decision']}")

            st.write(f"Risk Score: {result['risk_score']}")
            st.write(f"Response Code: {result['response_code']}")
            st.write("Reasons:", ", ".join(result["reason"]))

        else:
            st.error(f"Error API: {response.status_code}")
            st.write(response.text)

    except Exception as e:
        st.error(f"Error conexión: {e}")
