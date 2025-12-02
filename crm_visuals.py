import sqlite3
import pandas as pd

# Connect to your SQLite database using the full path
conn = sqlite3.connect("/Users/suhan/Documents/SQL Projects/crm_customer_insights_project/crm_customer_insights")

# Test by reading customers table
df_customers = pd.read_sql_query("SELECT * FROM customers;", conn)
print(df_customers)

# Read VIP customer query into a DataFrame
vip_query = """
SELECT 
    c.customer_id,
    c.first_name || ' ' || c.last_name AS full_name,
    SUM(t.amount) AS total_spent,
    SUM(ca.opened) AS campaigns_opened,
    SUM(ca.clicked) AS campaigns_clicked,
    ROUND(100.0 * SUM(ca.opened)/COUNT(ca.campaign_id), 2) AS open_rate,
    ROUND(100.0 * SUM(ca.clicked)/COUNT(ca.campaign_id), 2) AS click_rate,
    CASE 
        WHEN SUM(t.amount) >= 1000 AND ROUND(100.0 * SUM(ca.opened)/COUNT(ca.campaign_id),2) >= 50 THEN 'VIP'
        WHEN SUM(t.amount) >= 500 THEN 'High Value'
        ELSE 'Regular'
    END AS customer_segment
FROM customers c
LEFT JOIN transactions t ON c.customer_id = t.customer_id
LEFT JOIN campaigns ca ON c.customer_id = ca.customer_id
GROUP BY c.customer_id, full_name
ORDER BY total_spent DESC;
"""

df_vip = pd.read_sql_query(vip_query, conn)

# Preview the data
print(df_vip)

import matplotlib.pyplot as plt

# Bar chart: Total spend per customer
plt.figure(figsize=(8,5))
plt.bar(df_vip['full_name'], df_vip['total_spent'], color='skyblue')
plt.title('Total Spend per Customer')
plt.xlabel('Customer')
plt.ylabel('Total Spend')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("total_spend_per_customer.png")  # saves the figure in your current folder
plt.show()

# Stacked bar chart: Campaigns opened vs clicked
plt.figure(figsize=(8,5))

# Bars
plt.bar(df_vip['full_name'], df_vip['campaigns_opened'], label='Opened', color='skyblue')
plt.bar(df_vip['full_name'], df_vip['campaigns_clicked'], label='Clicked', color='salmon', bottom=df_vip['campaigns_opened'])

plt.title('Campaign Engagement per Customer')
plt.xlabel('Customer')
plt.ylabel('Number of Campaigns')
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.savefig("campaign_engagement_per_customer.png")  # optional: saves image
plt.show()

# Pie chart: Customer segments
segment_counts = df_vip['customer_segment'].value_counts()

plt.figure(figsize=(6,6))
plt.pie(segment_counts, labels=segment_counts.index, autopct='%1.1f%%', colors=['gold', 'skyblue', 'lightgray'], startangle=140)
plt.title('Customer Segments')
plt.tight_layout()
plt.savefig("customer_segments.png")  # optional: saves the image
plt.show()

