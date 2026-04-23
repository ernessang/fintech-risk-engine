import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Fintech Risk Dashboard", layout="wide")

st.title("💳 Fintech Risk Dashboard")

# Inicializar historial
if "history" not in st.session_state:
    st.session_state.history = []

# --- INPUT ---
st.subheader("🧾 Nueva transacción")

amount = st.number_input("Monto", min_value=0.0, value=100.0)
country = st.text_input("País", value="MX")
merchant = st.text_input("Comercio", value="AMAZON")
tokenized = st.checkbox("¿Tokenizada?", value=True)

# --- BOTÓN ---
if st.button("Analizar transacción"):

    tx = {
        "amount": amount,
        "country": country,
        "merchant": merchant,
        "tokenized": tokenized
    }

    try:
        response = requests.post(
            "http://127.0.0.1:8000/analyze-transaction",
            json=tx
        )
        result = response.json()

        # Guardar en historial
        st.session_state.history.append({
            "amount": amount,
            "merchant": merchant,
            "decision": result["decision"],
            "risk_score": result["risk_score"]
        })

        # Mostrar resultado actual
        st.subheader("📊 Resultado actual")
        st.write(f"Decision: {result['decision']}")
        st.write(f"Risk Score: {result['risk_score']}")
        st.write(f"Response Code: {result['response_code']}")
        st.write("Reasons:", ", ".join(result["reason"]))

    except Exception as e:
        st.error(f"Error: {e}")

# --- HISTORIAL ---
if st.session_state.history:
    st.subheader("📋 Historial de transacciones")
    df = pd.DataFrame(st.session_state.history)
    st.dataframe(df, use_container_width=True)

    st.subheader("📊 Riesgo por transacción")
    st.bar_chart(df["risk_score"])
