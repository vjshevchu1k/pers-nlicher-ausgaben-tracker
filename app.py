
---

### 🧠 **Код файлу `app.py`**

```python
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Persönlicher Ausgaben-Tracker", page_icon="💰", layout="wide")

st.title("💰 Persönlicher Ausgaben-Tracker")
st.markdown("Ein einfaches Tool zur Verwaltung und Visualisierung deiner Finanzen. 💸")

# --- Daten laden oder erstellen ---
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data.csv")
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Datum", "Kategorie", "Beschreibung", "Betrag", "Typ"])
    return df

df = load_data()

# --- Eingabeformular ---
st.sidebar.header("➕ Neue Transaktion hinzufügen")

with st.sidebar.form("add_transaction"):
    datum = st.date_input("Datum", datetime.today())
    kategorie = st.selectbox("Kategorie", ["Essen", "Transport", "Freizeit", "Miete", "Sonstiges"])
    beschreibung = st.text_input("Beschreibung")
    betrag = st.number_input("Betrag (€)", min_value=0.0, step=0.5)
    typ = st.selectbox("Typ", ["Einnahme", "Ausgabe"])
    submitted = st.form_submit_button("Hinzufügen")

    if submitted and betrag > 0:
        new_row = {"Datum": datum, "Kategorie": kategorie, "Beschreibung": beschreibung, "Betrag": betrag, "Typ": typ}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv("data.csv", index=False)
        st.success("✅ Transaktion erfolgreich hinzugefügt!")

# --- Datenübersicht ---
st.subheader("📋 Übersicht deiner Transaktionen")
st.dataframe(df)

if not df.empty:
    df["Datum"] = pd.to_datetime(df["Datum"])
    df["Monat"] = df["Datum"].dt.to_period("M").astype(str)

    # Einnahmen/Ausgaben zusammenfassen
    df["Betrag_signed"] = df.apply(lambda x: x["Betrag"] if x["Typ"] == "Einnahme" else -x["Betrag"], axis=1)
    monatliche_summe = df.groupby("Monat")["Betrag_signed"].sum().reset_index()

    st.subheader("📈 Monatlicher Saldo")
    fig = px.line(monatliche_summe, x="Monat", y="Betrag_signed", markers=True,
                  title="Monatliche Bilanz", labels={"Betrag_signed": "Saldo (€)"})
    st.plotly_chart(fig, use_container_width=True)

    # Kategorienanalyse
    kategorie_summe = df.groupby("Kategorie")["Betrag_signed"].sum().reset_index()
    st.subheader("🍕 Ausgaben nach Kategorie")
    fig2 = px.pie(kategorie_summe, names="Kategorie", values="Betrag_signed", title="Verteilung der Ausgaben")
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")
st.caption("© 2025 – Entwickelt von Vitalii Shevchuk 🇺🇦")
