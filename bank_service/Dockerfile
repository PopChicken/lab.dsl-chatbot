FROM python:3.10.0-buster

COPY requirements.txt /bank_service/
WORKDIR /bank_service/
RUN pip install -r requirements.txt

FROM python:3.10.0-alpine3.15

COPY . /bank_service/
WORKDIR /bank_service/

COPY --from=0 /usr/local/lib/python3.10/site-packages/ \
    /usr/local/lib/python3.10/site-packages/

RUN rm requirements.txt

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "--noreload"]