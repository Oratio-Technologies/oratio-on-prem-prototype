#!/bin/bash
# filepath: restart_bytewax.sh

# Log file to track restarts
LOG_FILE="bytewax_restarts.log"

echo "Starting Bytewax monitoring script at $(date)" | tee -a $LOG_FILE

# Function to timestamp log messages
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a $LOG_FILE
}

# Function to run the command and restart it if it fails
run_with_restart() {
    while true; do
        log "Starting bytewax process..."
        
        # Run the bytewax command
        uv run python -m bytewax.run main.py
        
        # Capture the exit code
        EXIT_CODE=$?
        
        # Log the exit
        log "Bytewax process exited with code $EXIT_CODE"
        
        # If the script was terminated by SIGINT (Ctrl+C) or SIGTERM, exit cleanly
        if [ $EXIT_CODE -eq 130 ] || [ $EXIT_CODE -eq 143 ]; then
            log "Detected clean shutdown signal. Exiting monitoring script."
            exit 0
        fi
        
        # Wait a bit before restarting to avoid rapid restart loops
        log "Waiting 5 seconds before restarting..."
        sleep 5
    done
}

# Trap Ctrl+C to exit cleanly
trap "log 'Received interrupt signal. Shutting down.'; exit 0" INT TERM

# Run the main function
run_with_restart