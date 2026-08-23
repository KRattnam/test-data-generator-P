FROM python:3.14-slim as base

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONNUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/* # clean up apt cache to keep image small

COPY pyproject.toml .

RUN pip install --no-cache-dir -e.

FROM base as development

RUN pip install --np-cahce-dir -e ".[dev]"

COPY . .
RUN  mkdir -p/app/exports

EXPOSE 8000

CMD ["uvicorn", "tdg.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

FROM base as PRODUCTION

COPY tdg/ ./tdg/
COPY profiles/ ./profiles/
COPY pyproject.toml .

RUN mkdir -p /app/exports

EXPOSE 8000

CMD ["uvicorn", "tdg.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]


