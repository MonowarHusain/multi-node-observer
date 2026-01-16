# Use a lightweight Python base image
FROM python:3.9-slim

# Install the ping utility (required for network monitoring)
RUN apt-get update && apt-get install -y iputils-ping && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install the Redis client for communication
RUN pip install redis

# Copy the local source code into the container
COPY . .

# Start the worker script by default
CMD ["python", "worker.py"]