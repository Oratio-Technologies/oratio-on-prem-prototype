#!/bin/bash

while true; do
    echo "Starting pipeline..."
    uv run python -m bytewax.run main.py
    echo "Pipeline exited. Restarting in 5 seconds..."
    sleep 5
done
