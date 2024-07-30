# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app


# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy dependency files
COPY pyproject.toml poetry.lock* /app/


# Install dependencies
RUN poetry install --no-root --no-dev


# Copy the current directory contents into the container at /app
COPY . /app


# Copy the rest of the frontend code
# COPY . /app/

# Make port 8501 available to the world outside this container
EXPOSE 8501

# Define environment variable
# ENV PORT=8501

# Run Streamlit when the container launches
CMD ["poetry", "run", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]


