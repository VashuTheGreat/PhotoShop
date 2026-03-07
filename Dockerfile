# Use a slim Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

# Set working directory
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy project files
COPY . /app/

# Create the from-root marker if missing (ensuring logger works)
RUN touch .from-root

# Install dependencies using uv sync
RUN uv sync --frozen --no-dev

# Expose the application port
EXPOSE 8000

# Set environment variables
ENV HOST=0.0.0.0
ENV PORT=8000

# Run the application
CMD ["uv", "run", "main.py"]
