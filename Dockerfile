FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=0 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN addgroup --system audit \
    && adduser --system --ingroup audit audit

COPY requirements.txt ./
RUN python -m pip install --upgrade pip \
    && python -m pip install --requirement requirements.txt

COPY . .
RUN chown -R audit:audit /app

USER audit

CMD ["sh", "-c", "python -m pytest -q && python scripts/check_all.py && python scripts/check_full_coverage.py && python scripts/check_full_coverage.py --strict-theory && python scripts/check_lean_coverage.py && python scripts/compile_registry.py"]
