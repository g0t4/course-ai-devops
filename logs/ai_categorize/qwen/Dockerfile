FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /src
COPY pyproject.toml .
COPY uv.lock .
RUN uv sync --frozen

COPY categorize_daemon.py .
EXPOSE 3000

CMD ["uv", "run", "categorize_daemon.py"]
