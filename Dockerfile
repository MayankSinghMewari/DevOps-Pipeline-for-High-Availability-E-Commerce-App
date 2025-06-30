# Use a lightweight Python base image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Set environment variables for Python to optimize container behavior
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Copy only the requirements file first to leverage Docker's cache
# This ensures pip install step is re-run only if requirements.txt changes
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
# This copies app.py, mongo-init.js, README.md, etc.
COPY . .

# Create a non-root user for security (Good practice!)
RUN useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose the port Streamlit runs on (default for Streamlit)
EXPOSE 8501

# Health check (as defined in your original Dockerfile)
# This is useful if you were to run the container directly with `docker run`
# When using docker-compose, the healthcheck in docker-compose.yml takes precedence
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Command to run the Streamlit application
CMD ["streamlit", "run", "app.py", \
    "--server.port=8501", \
    "--server.address=0.0.0.0", \
    "--server.headless=true", \
    "--server.fileWatcherType=none", \
    "--browser.gatherUsageStats=false"]