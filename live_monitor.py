import sqlite3
import time
import os

def fetch_live_data():
    # Connect to the local SQLite database
    conn = sqlite3.connect('network_stats.db')
    cursor = conn.cursor()

    try:
        while True:
            # Clear the terminal screen for a 'live' dashboard feel
            # Use 'cls' for Windows, 'clear' for Linux/Mac
            os.system('clear') 

            print("="*60)
            print(f"{'LIVE NETWORK MONITOR (DistriPulse)':^60}")
            print("="*60)
            print(f"{'Timestamp':<25} | {'Target Site':<20} | {'Status':<7} | {'Latency':<10}")
            print("-"*60)

            # SQL Query to fetch the last 15 entries from the logs
            # This uses your SQL skills to get the most recent data first
            cursor.execute('''
                SELECT timestamp, target, status, latency_ms 
                FROM monitoring_logs 
                ORDER BY id DESC 
                LIMIT 15
            ''')
            
            rows = cursor.fetchall()

            for row in rows:
                timestamp, target, status, latency = row
                # Formatting the output for better readability
                print(f"{timestamp:<25} | {target:<20} | {status:<7} | {latency:<10}ms")

            print("-"*60)
            print("Press Ctrl+C to stop the live monitor...")
            
            # Refresh rate: 1 second
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nClosing Live Monitor...")
    finally:
        conn.close()

if __name__ == "__main__":
    fetch_live_data()