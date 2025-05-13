# ---- Builder Stage ----
FROM python:3.12-slim AS builder

WORKDIR /app

# Install build dependencies (if any)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements to leverage Docker cache
COPY requirements.txt .

# Install dependencies in a virtual environment
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# ---- Final Stage ----
FROM python:3.12-slim

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Ensure venv Python and pip are used by default
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code
COPY src/ src/
COPY server.py .
COPY requirements.txt .
# Expose port if using HTTP transport (optional)
EXPOSE 8000

# Default command (can be overridden)
CMD ["python", "server.py"]