# Stage 1: Build environment using UV
FROM python:3.14-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvbin/uv

WORKDIR /workorder-backend
COPY pyproject.toml ./

# Install dependencies into a virtual environment using UV
RUN /uvbin/uv venv /workorder-backend/.venv && \
    /uvbin/uv pip install --no-cache -r pyproject.toml

# Stage 2: Runtime environment
FROM python:3.14-slim
WORKDIR /workorder-backend

# 1. Copy the project files first
COPY . /workorder-backend

# 2. Overwrite with the clean virtual environment from the builder stage
COPY --from=builder /workorder-backend/.venv /workorder-backend/.venv

ENV PATH="/workorder-backend/.venv/bin:$PATH"
EXPOSE 8000

# 3. Fixed entry point to match your 'app' directory structure
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]