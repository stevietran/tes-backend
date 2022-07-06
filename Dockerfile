FROM python:3.8 as requirements-stage

# install poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV PATH="${PATH}:/root/.poetry/bin"
 
# create dir and install packages
WORKDIR /app
ENV PYTHONPATH="/app"
COPY . /app/
RUN poetry install

RUN chmod +x ./prestart.sh
RUN chmod +x ./run.sh

CMD ["bash", "-c", "poetry run ./prestart.sh ; poetry run ./run.sh"]