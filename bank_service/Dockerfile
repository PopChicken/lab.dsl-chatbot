FROM python:3.10.0-buster

COPY requirements.txt /bank_service/
WORKDIR /bank_service/
RUN pip install -r requirements.txt -i https://mirrors.cloud.tencent.com/pypi/simple

FROM python:3.10.0-alpine3.15

COPY . /bank_service/
WORKDIR /bank_service/

COPY --from=0 /usr/local/lib/python3.10/site-packages/ \
    /usr/local/lib/python3.10/site-packages/

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories && \
    apk add gcc musl-dev python3-dev libffi-dev openssl-dev cargo && \
    pip install cryptography -i https://mirrors.cloud.tencent.com/pypi/simple && \
    apk del gcc musl-dev python3-dev libffi-dev openssl-dev cargo

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "--noreload"]