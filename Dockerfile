FROM python:3.9-slim

WORKDIR /project

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /project/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /project/requirements.txt

COPY ./apps /project/apps
COPY ./modules /project/modules
COPY ./config.ini /project/config.ini

CMD ["uvicorn", "apps.api.rest.main:app", "--host", "0.0.0.0", "--port", "5000"]