# Build stage - Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.13-alpine AS builder

# Install the project into `/app`
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Install git and build dependencies for ClickHouse client
RUN --mount=type=cache,target=/var/cache/apk \
    apk add --no-cache git build-base

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=README.md,target=README.md \
    uv sync --locked --no-install-project --no-dev

# Then, add the rest of the project source code and install it
# Installing separately from its dependencies allows optimal layer caching
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev --no-editable

# Production stage - Use minimal Python image
FROM python:3.13-alpine

# Install runtime dependencies for ClickHouse client
RUN --mount=type=cache,target=/var/cache/apk \
    apk add --no-cache \
    ca-certificates \
    tzdata \
    && rm -rf /tmp/*

# Create a non-root user for security
RUN addgroup -g 1001 -S mcp && \
    adduser -u 1001 -S mcp -G mcp

# Set the working directory
WORKDIR /app

# Copy the virtual environment from the builder stage
COPY --from=builder --chown=mcp:mcp /app/.venv /app/.venv

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Switch to non-root user
USER mcp

# Add health check for the MCP server
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import chmcp; print('MCP ClickHouse Cloud & On-Prem server is healthy')" || exit 1

# Add metadata labels
LABEL org.opencontainers.image.title="MCP ClickHouse Cloud & On-Prem Server" \
      org.opencontainers.image.description="A comprehensive Model Context Protocol server for ClickHouse database operations and cloud management" \
      org.opencontainers.image.version="0.1.1" \
      org.opencontainers.image.authors="Badr Ouali <badr.ouali@outlook.fr>" \
      org.opencontainers.image.source="https://github.com/oualib/chmcp" \
      org.opencontainers.image.licenses="Apache-2.0"

# Run the MCP ClickHouse Cloud & On-Prem server by default
CMD ["python", "-m", "chmcp.main"]