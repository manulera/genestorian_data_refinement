FROM python:3.9

WORKDIR /pipeline

RUN pip install poetry 
RUN pip install nltk
RUN pip install toml

COPY ./ /pipeline/

RUN poetry config virtualenvs.create false
RUN poetry install --without dev
RUN poetry shell

COPY . /pipeline

