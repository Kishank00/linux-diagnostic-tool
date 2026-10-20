FROM python:3.12-slim

# Copy uv into the image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Configure Python and uv
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

# Create a non-root user
RUN useradd --create-home --uid 10001 appuser \
    && chown appuser:appuser /app

USER appuser

# Install dependencies from the lockfile
COPY --chown=appuser:appuser pyproject.toml uv.lock ./
RUN uv sync --locked --no-install-project --no-dev

# Copy the application: the API, the anomaly-detection code it imports,
# and the trained model it loads at startup
COPY --chown=appuser:appuser sysdiag/ ./sysdiag/
COPY --chown=appuser:appuser aiops/ ./aiops/
COPY --chown=appuser:appuser models/ ./models/

# Use the project's virtual environment
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

CMD ["uvicorn", "sysdiag.api.main:app", "--app-dir", "/app", "--host", "0.0.0.0", "--port", "8000"]
