# docker/Dockerfile

FROM python:3.10-slim

LABEL maintainer="z3r0@triad.ecosystem"
LABEL description="TRIAD Ecosystem - Autonomous Cyber Evolution"

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    make \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY src/ ./src/
COPY config/ ./config/
COPY run.py .
COPY setup.py .

# Create directories for data
RUN mkdir -p /data/snapshots /data/logs /data/reports

# Set environment variables
ENV PYTHONPATH=/app
ENV TRIAD_ENV=docker
ENV TRIAD_ISOLATED=true

# Expose dashboard port
EXPOSE 8765

# Run with isolated network
CMD ["python", "run.py", "--preset", "default", "--dashboard-port", "8765"]
