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

## URL設計

|    URL    |    メソッド    |    認証    |    処理内容    |
|:------------------|:------------------|:------------------:|:-----------------|
|    /admin    |    GET   |    🔑    |    管理者ページ表示    |
|    /register    |    GET   |    -    |    登録ページ表示    |
|    /register    |    POST   |    -    |    登録処理    |
|    /todo/{username}/{year}/{month}/{day}    |    GET   |    🔑    |    予定詳細ページ表示    |
|    /done    |    POST   |    🔑    |    終了したことをpost    |
|    /add    |    POST   |    🔑    |    予定追加    |
|    /delete/{task_id}    |    GET   |    🔑    |    予定削除    |
|    /get    |    GET   |    🔑    |    タスク情報取得    |
|    /add_task    |    POST   |    🔑    |    タスク追加    |
|    /logout    |    GET   |    🔑    |    ログアウト    |



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
