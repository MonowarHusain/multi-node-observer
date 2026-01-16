import sqlite3

# Connect to your local database
conn = sqlite3.connect('network_stats.db')
cursor = conn.cursor()

print("--- Network Performance Summary ---")

# Query: Average latency per target
cursor.execute('''
    SELECT target, 
           COUNT(*) as checks, 
           ROUND(AVG(latency_ms), 2) as avg_latency 
    FROM monitoring_logs 
    GROUP BY target
''')

rows = cursor.fetchall()
for row in rows:
    print(f"Target: {row[0]} | Total Checks: {row[1]} | Avg Latency: {row[2]}ms")

conn.close()
