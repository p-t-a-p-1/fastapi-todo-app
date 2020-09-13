# スケジュール管理アプリ

## 開発言語

* FastAPI - Pythonのフレームワーク
* Jinja2 - Pythonのテンプレートエンジン
* MySQL - DB
* Bulma - CSSフレームワーク
* Docker(Docker-compose) - 環境整備

## python使用パッケージ
* fastapi フレームワーク
* uvicorn サーバー
* starlette サーバー
* sqlalchemy DB操作のためのORM
* jinja2 テンプレートエンジン
* aiofiles ファイル操作
* mysqlclient mysql関連
* python-multipart 複数request
* datetime 日付

## ローカル動作方法

```
docker-compose build
```

```
docker-compose up -d
```

http://localhost:8000

## 動作イメージ
![screencapture-localhost-8000-admin-2020-06-20-10_04_04](https://user-images.githubusercontent.com/51960141/85187809-780f3300-b2dd-11ea-8457-64db00ddaf7a.png)
