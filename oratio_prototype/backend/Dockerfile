# Use the official Python image
FROM python:3.10-slim AS base

# Set working directory
WORKDIR /app

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy dependency files
COPY pyproject.toml poetry.lock* /app/

# Install dependencies
RUN poetry install --no-root --no-dev

# Copy the application code
COPY . /app

# Expose the port FastAPI is running on
EXPOSE 8080

# Start the FastAPI app
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
