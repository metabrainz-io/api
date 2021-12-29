FROM python:latest

ENV PYTHONUNBUFFERED 1
ENV API_ROOT=/api
ENV API_HOST="localhost"

WORKDIR /api
COPY . ./

RUN apt-get -y update && apt-get install -y nano
RUN pip install -r requirements.txt

CMD [ "python3", "restapi/manage.py" , "runserver", "0.0.0.0:8000" ]