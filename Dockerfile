# Use a Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies needed for PyTorch & transformers
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files into container
COPY . .

# Hugging Face Spaces runs apps on port 7860
ENV PORT=7860

# Expose that port
EXPOSE 7860

# Start flask using gunicorn (same as Render)
CMD ["gunicorn", "app:app", "--workers", "1", "--threads", "2", "--timeout", "600", "--bind", "0.0.0.0:7860"]
