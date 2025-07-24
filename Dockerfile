# Stage 1: Build the application
FROM python:3.10-slim-buster AS builder

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Create the final image
FROM python:3.10-slim-buster

WORKDIR /app

# Copy only the installed packages from the builder stage
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
# Copy application code
COPY main.py .

# Create a non-root user and switch to it for security
RUN adduser --system --group appuser
USER appuser

# Expose the port FastAPI runs on
EXPOSE 8000

# Set environment variables for production
ENV PYTHONUNBUFFERED=1 \
    UVICORN_HOST=0.0.0.0 \
    UVICORN_PORT=8000 \
    LOG_LEVEL=info

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "$(UVICORN_HOST)", "--port", "$(UVICORN_PORT)", "--log-level", "$(LOG_LEVEL)"]