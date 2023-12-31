FROM python:3.10.4-buster AS production-environment

ENV PYTHONDONTWRITEBYTECODE=true \
    PYTHONIOENCODING=UTF-8 \
    POETRY_VERSION=1.3.2 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false

ENV PATH="${POETRY_HOME}/bin:${PATH}"

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        build-essential

RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN poetry install --no-dev --no-root --no-interaction


FROM production-environment AS search-image

COPY search ./search

ENTRYPOINT ["python3", "-m", "search"]


FROM production-environment AS development-environment

RUN poetry install --no-root --no-interaction


FROM development-environment AS init-image

COPY search ./search
COPY migrations ./migrations

ENTRYPOINT ["python3", "-m", "migrations"]
