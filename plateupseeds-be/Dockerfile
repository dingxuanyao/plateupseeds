FROM python:3.10.7-buster
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./src /code/src
COPY ./alembic /code/alembic
COPY ./alembic.ini /code/alembic.ini
COPY ./.env* /code/
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]
