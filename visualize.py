import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

def plot_latency():
    # Connect to the SQLite database
    conn = sqlite3.connect('network_stats.db')
    
    # Load the data into a Pandas DataFrame using SQL
    # This queries the logs collected by your aggregator
    query = "SELECT target, latency_ms, timestamp FROM monitoring_logs"
    df = pd.read_sql_query(query, conn)
    
    # Close connection
    conn.close()

    # Data Cleaning: Filter out rows where latency is 'N/A' (target was down)
    df = df[df['latency_ms'] != 'N/A']
    df['latency_ms'] = df['latency_ms'].astype(float)
    
    # Convert timestamp to datetime objects for accurate time plotting
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Initialize the plot figure
    plt.figure(figsize=(10, 6))

    # Group data by target and plot each target as a separate line
    # This allows comparing Google, GitHub, and your Local Router on one graph
    for target, group in df.groupby('target'):
        plt.plot(group['timestamp'], group['latency_ms'], label=target, marker='o', markersize=4)

    # Adding plot metadata and labels
    plt.title('Multi-Node Network Latency Report')
    plt.xlabel('Timestamp')
    plt.ylabel('Latency (ms)')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Rotate time labels on X-axis for better visibility
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save the output image
    output_name = 'latency_report.png'
    plt.savefig(output_name)
    print(f"Graph successfully generated and saved as {output_name}")
    
    # Display the plot window
    plt.show()

if __name__ == "__main__":
    plot_latency()