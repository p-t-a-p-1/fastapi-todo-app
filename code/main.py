from fastapi import FastAPI
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from typing import List
from starlette.middleware.cors import CORSMiddleware
from db import session
from models import UserTable, TaskTable


app = FastAPI(
    title='FastAPIで作成するTODOアプリ',
    description='シンプルなTODOアプリです',
    version='0.9 beta'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.mount('/static', StaticFiles(directory='static'), name='static')

templates = Jinja2Templates(directory='templates')


@app.get('/')
def index(request: Request):
    return templates.TemplateResponse(
        'index.html',
        {
            'request': request
        }
    )


@app.get('/admin')
def admin(request: Request):
    # ユーザーとタスクを取得
    users = session.query(UserTable).all()
    tasks = session.query(TaskTable).all()
    session.close()

    return templates.TemplateResponse(
        'admin.html',
        {
            'request': request,
            'username': 'admin',
            'users': users,
            'tasks': tasks,
        }
    )


@app.get('/users')
def read_users():
    users = session.query(UserTable).all()
    return users
