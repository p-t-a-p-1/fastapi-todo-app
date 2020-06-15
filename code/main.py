from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from starlette.status import HTTP_401_UNAUTHORIZED
from starlette.middleware.cors import CORSMiddleware

from typing import List

import db
from models import UserTable, TaskTable

import hashlib

security = HTTPBasic()

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
def admin(request: Request, credentials: HTTPBasicCredentials = Depends(security)):
    # Basic認証で受け取った情報
    username = credentials.username
    password = hashlib.md5(credentials.password.encode()).hexdigest()

    # DBからユーザー名が一致する情報を取得
    user = db.session.query(UserTable).filter(UserTable.username == username).first()
    tasks = db.session.query(TaskTable).filter(TaskTable.user_id == user.id).all() if user is not None else []
    db.session.close()

    # 該当ユーザーがいない場合
    if user is None or user.password != password:
        error = 'ユーザー名かパスワードが間違っています'
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail=error,
            headers={"WWW-Authenticate": "Basic"},
        )

    return templates.TemplateResponse(
        'admin.html',
        {
            'request': request,
            'user': user,
            'tasks': tasks,
        }
    )


@app.get('/users')
def read_users():
    users = db.session.query(UserTable).all()
    db.session.close()
    return users


@app.get('/tasks')
def read_tasks():
    tasks = db.session.query(TaskTable).all()
    db.session.close()
    return tasks


@app.get('/register')
def read_register(request: Request):
    return templates.TemplateResponse(
        'register.html',
        {
            'request': request,
            'username': '',
            'error': []
        }
    )


@app.post('/register')
def create_register(request: Request):
    pass
