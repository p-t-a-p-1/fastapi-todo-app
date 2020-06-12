FROM python:3.8-alpine

WORKDIR /usr/src/server

COPY requirements.txt .
# コンテナ内で必要なパッケージをインストール
RUN apk add --no-cache build-base mariadb-connector-c-dev \
 && pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt \
 && apk del build-base

# COPY main.py .
# COPY static/ static/
# COPY templates/ templates/

EXPOSE 8000
# FastAPIを8000ポートで待機
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]