# context is set by docker-compose.yml:
# ./farmer-market-server

FROM python:3.12.5-alpine3.19

RUN pip install --upgrade pip

COPY .build/requirements/base_requirements.txt /tmp/base_requirements.txt
RUN pip install -r /tmp/base_requirements.txt

COPY .build/requirements/requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY . /app
WORKDIR /app

ENTRYPOINT ["sh", "./.build/entrypoint.sh"]

