import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Verbindung zur DB
conn = sqlite3.connect('sales.db')

# Daten laden
data = pd.read_sql_query("SELECT * FROM sales", conn)

st.title("Verkaufsdaten Dashboard")

# Gesamtumsatz pro Produkt
st.header("1️⃣ Gesamtumsatz pro Produkt")
revenue_by_product = data.groupby('product')['total_price'].sum().sort_values(ascending=False)
st.bar_chart(revenue_by_product)

# Durchschnittlicher Bestellwert
st.header("2️⃣ Durchschnittlicher Bestellwert")
avg_order_value = data['total_price'].mean()
st.metric(label="Durchschnittlicher Bestellwert", value=f"{avg_order_value:.2f} €")

# Top-Kunden nach Umsatz
st.header("3️⃣ Top-Kunden nach Umsatz")
revenue_by_customer = data.groupby('customer_name')['total_price'].sum().sort_values(ascending=False)
st.dataframe(revenue_by_customer.reset_index().rename(columns={'total_price': 'Umsatz'}))

# Verteilung der Bestellungen pro Produkt
st.header("4️⃣ Anzahl Bestellungen pro Produkt")
order_counts = data['product'].value_counts()
fig, ax = plt.subplots()
sns.barplot(x=order_counts.index, y=order_counts.values, ax=ax)
ax.set_ylabel('Anzahl Bestellungen')
ax.set_xlabel('Produkt')
st.pyplot(fig)

# Optional: Filter nach Kunde
st.header("5️⃣ Filter: Umsatz nach Kunde")
selected_customer = st.selectbox("Kunden auswählen", options=data['customer_name'].unique())
customer_data = data[data['customer_name'] == selected_customer]
st.write(customer_data)

conn.close()
