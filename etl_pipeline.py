import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# Beispiel Verkaufsdaten
data = [
    {'order_id': 1, 'product': 'Laptop', 'quantity': 2, 'price_per_unit': 1500, 'customer_name': 'Max Müller'},
    {'order_id': 2, 'product': 'Smartphone', 'quantity': 1, 'price_per_unit': 800, 'customer_name': 'Anna Schmidt'},
    {'order_id': 3, 'product': 'Tablet', 'quantity': 4, 'price_per_unit': 400, 'customer_name': 'Max Müller'},
    {'order_id': 4, 'product': 'Smartwatch', 'quantity': 5, 'price_per_unit': 200, 'customer_name': 'Julia Klein'},
]

# ETL-Prozess
df = pd.DataFrame(data)
df['total_price'] = df['quantity'] * df['price_per_unit']

conn = sqlite3.connect('sales.db')
df.to_sql('sales', conn, if_exists='replace', index=False)
print("✅ Daten in sales.db geladen.")

# SQL-Abfragen und Ausgabe
queries = {
    "Gesamtumsatz pro Produkt": """
        SELECT product, SUM(total_price) AS total_revenue
        FROM sales
        GROUP BY product
        ORDER BY total_revenue DESC
    """,
    "Durchschnittlicher Bestellwert": """
        SELECT ROUND(AVG(total_price), 2) AS avg_order_value
        FROM sales
    """,
    "Top-Kunde nach Umsatz": """
        SELECT customer_name, SUM(total_price) AS customer_revenue
        FROM sales
        GROUP BY customer_name
        ORDER BY customer_revenue DESC
        LIMIT 1
    """
}

for description, query in queries.items():
    print(f"\n📌 {description}:\n-- Query:\n{query}")
    result = pd.read_sql_query(query, conn)
    print(result)

# Visualisierung: Gesamtumsatz pro Produkt
def plot_total_revenue():
    df_revenue = pd.read_sql_query(queries["Gesamtumsatz pro Produkt"], conn)
    plt.figure(figsize=(8,5))
    plt.bar(df_revenue['product'], df_revenue['total_revenue'], color='skyblue')
    plt.title('Gesamtumsatz pro Produkt')
    plt.xlabel('Produkt')
    plt.ylabel('Umsatz in €')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

plot_total_revenue()

conn.close()
