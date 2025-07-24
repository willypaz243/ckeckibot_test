FROM python:3.12-slim-bookworm

# The installer requires curl (and certificates) to download the release archive
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

# Download the latest installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"
ENV UV_LINK_MODE=copy

WORKDIR /app
COPY pyproject.toml .
COPY uv.lock .

RUN uv sync

CMD [ "uv", "run", "uvicorn", "--host", "0.0.0.0", "--port", "8000", "main:app" ]