import redis
import json
import sqlite3
import time

# Connect to local Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Database Setup
conn = sqlite3.connect('network_stats.db')
cursor = conn.cursor()

# Create Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS monitoring_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        target TEXT,
        status TEXT,
        latency_ms REAL,
        timestamp TEXT
    )
''')
conn.commit()

print("Aggregator is running and waiting for results from workers...")

try:
    while True:
        # Pull results from 'monitor_results' queue
        result_data = r.blpop("monitor_results", timeout=5)
        
        if result_data:
            data = json.loads(result_data[1].decode('utf-8'))
            
            # Use 'node_target' because the worker script sends it under this key
            target_val = data.get('node_target') or data.get('target')
            
            # Insert into SQL database
            cursor.execute('''
                INSERT INTO monitoring_logs (target, status, latency_ms, timestamp)
                VALUES (?, ?, ?, ?)
            ''', (target_val, data['status'], data['latency_ms'], data['timestamp']))
            
            conn.commit()
            print(f"Logged result for {target_val} | Latency: {data['latency_ms']}ms")
        
except KeyboardInterrupt:
    print("\nStopping Aggregator...")
    conn.close()