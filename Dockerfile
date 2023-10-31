FROM python:3.9

WORKDIR /pipeline

RUN pip install poetry
RUN poetry config virtualenvs.create false

COPY ./ /pipeline

RUN poetry install --no-dev
RUN sh install_local_dependency.sh

CMD ["sh", "docker_start.sh"]
