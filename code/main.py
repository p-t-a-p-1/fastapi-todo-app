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

# passwordで使用
import hashlib
# 正規表現
import re

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

# 任意の4〜20の英数字
pattern = re.compile(r'\w{4,20}')
# 任意の6〜20の英数字
pattern_pw = re.compile(r'\w{6,20}')
# emailの正規表現
pattern_mail = re.compile(r'^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$')


# トップ表示
@app.get('/')
def index(request: Request):
    return templates.TemplateResponse(
        'index.html',
        {
            'request': request
        }
    )


# 管理者ページ表示
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


# 全ユーザー一覧
@app.get('/users')
def read_users():
    users = db.session.query(UserTable).all()
    db.session.close()
    return users


# 全タスク一覧
@app.get('/tasks')
def read_tasks():
    tasks = db.session.query(TaskTable).all()
    db.session.close()
    return tasks


# 登録ページ表示
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


# 登録処理
@app.post('/register')
async def create_register(request: Request):
    # POSTされた情報取得
    data = await request.form()
    username = data.get('username')
    password = data.get('password')
    password_tmp = data.get('password_tmp')
    mail = data.get('mail')

    error = []

    # UserTableから登録しようとしてるユーザーがないか
    tmp_user = db.session.query(UserTable).filter(UserTable.username == username).first()

    # 登録に関するバリデーション
    if tmp_user is not None:
        error.append('同じユーザ名のユーザが存在します')
    if password != password_tmp:
        error.append('入力したパスワードが一致しません')
    if pattern.match(username) is None:
        error.append('ユーザ名は4〜20文字の半角英数字にしてください')
    if pattern_pw.match(password) is None:
        error.append('パスワードは6〜20文字の半角英数字にしてください')
    if pattern_mail.match(mail) is None:
        error.append('正しくメールアドレスを入力してください')

    # エラー含めviewに渡す
    if error:
        return templates.TemplateResponse(
            'register.html',
            {
                'request': request,
                'username': username,
                'error': error
            }
        )

    # 問題ない場合はUserTableに登録
    user = UserTable(username, password, mail)
    db.session.add(user)
    db.session.commit()
    db.session.close()

    return templates.TemplateResponse(
        'complete.html',
        {
            'request': request,
            'username': username
        }
    )
