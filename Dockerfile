FROM python:latest

ENV PYTHONUNBUFFERED 1
ENV API_ROOT=/api
ENV API_HOST="0.0.0.0"
ENV API_PORT=5000

RUN apt-get -y update && apt-get install -y \
    nano dos2unix net-tools nginx
    
WORKDIR /api
COPY . ./

RUN pip install -r requirements.txt
RUN sed -i -e 's/\r$//' ${API_ROOT}/scripts/*.sh

CMD [ "python3", "restapi/manage.py" , "runserver", "0.0.0.0:5000" ]