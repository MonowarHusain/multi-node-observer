import redis
import os
import subprocess
import time
import json

# Connect to the Redis service using the hostname defined in docker-compose
r = redis.Redis(host=os.environ.get('REDIS_HOST', 'localhost'), port=6379, db=0)

print("Network Observer Node is active...")

while True:
    # Wait and pop a task from the 'network_tasks' queue
    task = r.blpop("network_tasks", timeout=0)
    
    if task:
        target = task[1].decode('utf-8')
        
        # Execute ping command with 2 packets to measure latency
        res = subprocess.run(['ping', '-c', '2', target], capture_output=True, text=True)
        
        # Determine status: 0 return code means host is reachable
        status = "UP" if res.returncode == 0 else "DOWN"
        
        # Extract the average latency (ms) from the ping output
        latency = res.stdout.split('/')[-3] if status == "UP" else "N/A"
        
        result = {
            "node_target": target,
            "status": status,
            "latency_ms": latency,
            "timestamp": time.ctime()
        }
        
        # Push the observed result to the result queue
        r.rpush("monitor_results", json.dumps(result))
        print(f"[{status}] Observed: {target} | Latency: {latency}ms")