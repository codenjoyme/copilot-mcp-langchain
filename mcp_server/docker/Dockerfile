# Use Python 3.13.5 to match local development environment
FROM python:3.13.5-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files from parent directory
COPY mcp_server ./mcp_server
COPY install.sh ./install.sh

# Convert install.sh line endings and run for additional dependencies (ignore errors)
RUN if [ -f "./install.sh" ]; then \
        sed -i 's/\r$//' ./install.sh && \
        chmod +x ./install.sh && \
        (bash ./install.sh || echo "Install script completed with warnings"); \
    fi

# Clean up after installation
RUN rm -rf /root/.cache/pip

# Create default directory structure and copy default content
RUN mkdir -p /app/mcp_server/config && \
    mkdir -p /app/mcp_server/logs && \
    mkdir -p /app/mcp_server/projects

# Create a template directory with defaults for initialization
RUN mkdir -p /app/templates && \
    cp -r /app/mcp_server/config /app/templates/ && \
    cp -r /app/mcp_server/projects /app/templates/

# Accept EXPOSE_PORTS as build argument for logging purposes
ARG EXPOSE_PORTS="8000 8080 9000 9001"

# Log which ports will be exposed (actual port mapping happens at runtime via run scripts)
RUN echo "Configured ports: $EXPOSE_PORTS"

# Expose common ports (actual ports used will depend on MCP_PORTS in .env at runtime)
EXPOSE 8000 8080 9000 9001

# Set working directory to mcp_server
WORKDIR /app/mcp_server

# Run the MCP server using Python from virtual environment
CMD ["/app/.virtualenv/bin/python", "server.py"]
