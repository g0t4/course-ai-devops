FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /src
COPY pyproject.toml .
COPY uv.lock .
RUN uv sync --frozen

COPY server.py /src/
COPY templates /src/templates
EXPOSE 3000

CMD ["uv", "run", "server.py"]
