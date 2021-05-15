ARG PYTHON_ENV=python:3.11-slim
ARG POETRY_VERSION=1.6.1

FROM $PYTHON_ENV as build
# Allow statements and log messages to immediately appear in the logs
ENV PYTHONUNBUFFERED True

RUN apt-get update && \
    apt-get install --yes --no-install-recommends curl g++ libopencv-dev && \
    rm -rf /var/lib/apt/lists/*
RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=${POETRY_VERSION} python3 -

RUN mkdir -p /app
WORKDIR /app

COPY pyproject.toml poetry.lock ./

ENV PATH="/root/.local/bin:$PATH"
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-root

COPY detectron2 ./detectron2

RUN cd detectron2 && \
    python setup.py build && \
    python setup.py install

FROM $PYTHON_ENV as prod

# Allow statements and log messages to immediately appear in the logs
ENV PYTHONUNBUFFERED True
# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./
COPY magic-pdf.json /root

COPY --from=build /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=build /usr/lib/x86_64-linux-gnu /usr/lib/x86_64-linux-gnu
COPY --from=build /usr/local/bin/magic-pdf /usr/local/bin/magic-pdf
COPY --from=build /usr/local/bin/uvicorn /usr/local/bin/uvicorn

RUN python download_models.py

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "3000"]

