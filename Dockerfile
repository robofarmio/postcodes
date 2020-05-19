FROM ubuntu:20.04

ENV LANG="C.UTF-8" LC_ALL="C.UTF-8" PATH="/home/rf/.poetry/bin:/home/rf/.local/bin:$PATH" PIP_NO_CACHE_DIR="false"

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    python3 python3-pip python3-venv python-is-python3 curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN groupadd --gid 1000 rf && \
    useradd  --uid 1000 --gid rf --shell /bin/bash --create-home rf

USER 1000
RUN mkdir /home/rf/app
WORKDIR /home/rf/app

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/9f93df1140efd44f37d07fc04fe5eb9abdc105db/get-poetry.py | python
RUN poetry config virtualenvs.create false

COPY --chown=rf:rf pyproject.toml poetry.lock ./
RUN poetry install --no-interaction --no-root --ansi

COPY --chown=rf:rf . .
RUN poetry install --no-interaction --ansi

ENTRYPOINT ["postcodes"]
CMD ["--help"]
