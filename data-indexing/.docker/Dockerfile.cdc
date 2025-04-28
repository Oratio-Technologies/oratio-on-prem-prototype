# Use an official Python runtime as a parent image
FROM python:3.10-slim AS base

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    curl \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# Add Poetry to PATH
ENV PATH="/etc/poetry/bin:$PATH"

# Set the working directory
WORKDIR /app

# Copy the pyproject.toml and poetry.lock files from the 2-data-ingestion directory
COPY ../2-data-ingestion/pyproject.toml ../2-data-ingestion/poetry.lock* ./

# Install dependencies
RUN poetry install --no-root

# Copy the 2-data-ingestion and core directories
COPY ../2-data-ingestion /app/

# Set the PYTHONPATH environment variable
ENV PYTHONPATH=/app

# Command to run the script
CMD poetry run python /app/cdc.py && tail -f /dev/null
