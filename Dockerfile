# Dockerfile for Gemini CLI Agentic Workspace
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    openssh-client \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create sketches directory
RUN mkdir -p sketches

# Make scripts executable
RUN chmod +x gemini_workspace.py setup.sh

# Set environment variable for Python unbuffered output
ENV PYTHONUNBUFFERED=1

# Default command - interactive mode
CMD ["python", "gemini_workspace.py", "-i"]
