#!/bin/bash

# Docker container ID or name
CONTAINER_ID="10e95ee2f45f"

# Flag to track whether the container has been stopped
container_stopped=0

# Function to stop the Docker container
function stop_container {
    if [ $container_stopped -eq 0 ]; then
        echo "Stopping Docker container..."
        docker stop ${CONTAINER_ID}
        container_stopped=1
    fi
}

# Trap SIGINT (Ctrl+C) and SIGTERM signals to ensure the Docker container is stopped
trap stop_container SIGINT SIGTERM

# Start the Docker container
echo "Starting Docker container..."
docker start ${CONTAINER_ID} || { echo "Failed to start Docker container"; exit 1; }

# Start the FastAPI application
echo "Starting FastAPI application with Uvicorn..."
uvicorn main:app --reload --host 127.0.0.1 --port 8000 --log-level debug

# Ensure the Docker container is stopped when the script exits normally
stop_container