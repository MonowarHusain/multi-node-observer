import redis
import time

# Connect to local Redis mapping
r = redis.Redis(host='localhost', port=6379, db=0)

# List of target nodes to observe
# You can add your home server or local IP here
targets = ["google.com", "8.8.8.8", "github.com", "192.168.0.1"]

print("Multi-Node Orchestrator started. Sending pulses every 30 seconds...")

while True:
    for t in targets:
        # Push the target to the task queue
        r.rpush("network_tasks", t)
    
    # Wait for the next monitoring cycle
    time.sleep(30)