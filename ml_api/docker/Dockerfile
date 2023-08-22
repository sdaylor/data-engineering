FROM python:3.9
ENV PATH="${PATH}:/root/.local/bin"
WORKDIR /app

RUN curl --retry 5 -sSL https://install.python-poetry.org | python3 -

COPY pyproject.toml .
COPY poetry.lock .
COPY ml_api/. .

RUN poetry export --without-hashes -f requirements.txt --output requirements.txt
RUN pip install -r requirements.txt

CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]
