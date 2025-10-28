import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Persönlicher Ausgaben-Tracker", page_icon="💰", layout="wide")

st.title("💰 Persönlicher Ausgaben-Tracker")
st.markdown("Erstellt von **Vitalii Shevchuk** – Einfache Verwaltung und Analyse deiner Finanzen.")

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("expenses.csv")
        df["Datum"] = pd.to_datetime(df["Datum"], errors="coerce")
        return df
    except Exception:
        return pd.DataFrame(columns=["Datum", "Kategorie", "Betrag", "Beschreibung"])

df = load_data()

col1, col2, col3 = st.columns(3)
with col1:
    date = st.date_input("📅 Datum", datetime.today())
with col2:
    category = st.selectbox("📂 Kategorie", ["Essen", "Transport", "Freizeit", "Miete", "Einkauf", "Sonstiges"])
with col3:
    amount = st.number_input("💵 Betrag (€)", min_value=0.0, step=0.5)

desc = st.text_input("📝 Beschreibung")

if st.button("💾 Ausgabe hinzufügen"):
    new_row = {"Datum": date, "Kategorie": category, "Betrag": amount, "Beschreibung": desc}
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df["Datum"] = pd.to_datetime(df["Datum"], errors="coerce")
    df.to_csv("expenses.csv", index=False)
    st.success("✅ Ausgabe erfolgreich hinzugefügt!")

if not df.empty:
    st.subheader("📊 Übersicht der Ausgaben")

    df["Datum"] = pd.to_datetime(df["Datum"], errors="coerce")
    monthly_expenses = df.groupby(df["Datum"].dt.to_period("M"))["Betrag"].sum().reset_index()
    monthly_expenses["Datum"] = monthly_expenses["Datum"].astype(str)
    fig1 = px.line(monthly_expenses, x="Datum", y="Betrag", title="Monatliche Ausgaben (€)")
    st.plotly_chart(fig1, use_container_width=True)

    category_expenses = df.groupby("Kategorie")["Betrag"].sum().reset_index()
    fig2 = px.pie(category_expenses, names="Kategorie", values="Betrag", title="Ausgaben nach Kategorie")
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("📜 Alle Transaktionen")
    st.dataframe(df.sort_values("Datum", ascending=False))
else:
    st.info("🔎 Noch keine Daten vorhanden. Bitte füge eine Ausgabe hinzu.")
