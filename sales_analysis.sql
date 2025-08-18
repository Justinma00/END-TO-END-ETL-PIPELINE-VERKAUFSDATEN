-- 1️⃣ Gesamtumsatz pro Produkt
SELECT 
    product,
    SUM(total_price) AS total_revenue
FROM sales
GROUP BY product
ORDER BY total_revenue DESC;

-- 2️⃣ Durchschnittlicher Bestellwert
SELECT 
    ROUND(AVG(total_price), 2) AS avg_order_value
FROM sales;

-- 3️⃣ Top-Kunde nach Umsatz
SELECT 
    customer_name,
    SUM(total_price) AS customer_revenue
FROM sales
GROUP BY customer_name
ORDER BY customer_revenue DESC
LIMIT 1;
