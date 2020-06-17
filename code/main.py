from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import RedirectResponse

from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from starlette.status import HTTP_401_UNAUTHORIZED
from starlette.middleware.cors import CORSMiddleware
# from starlette.responses import RedirectResponse

from typing import List

import db
from models import UserTable, TaskTable

# passwordで使用
import hashlib
# 正規表現
import re

# カレンダー
from mycalendar import MyCalendar
from datetime import datetime
from datetime import timedelta

# Basic認証
from auth import basic_auth

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
@app.post('/admin')
def admin(request: Request, credentials: HTTPBasicCredentials = Depends(security)):
    # Basic認証で受け取った情報
    username = basic_auth(credentials)

    today = datetime.now()
    # 1週間後の日付
    next_w = today + timedelta(days=7)

    # DBからユーザー名が一致する情報を取得
    user = db.session.query(UserTable).filter(UserTable.username == username).first()
    tasks = db.session.query(TaskTable).filter(TaskTable.user_id == user.id).all() if user is not None else []
    db.session.close()

    # カレンダーをHTML形式で取得
    # 予定がある日付をdictのキーとして渡す
    cal = MyCalendar(
        username,
        {
            t.deadline.strftime('%Y%m%d'): t.done for t in tasks
        }
    )
    # カレンダーをHTMLで取得
    cal = cal.formatyear(today.year, 4)

    # 直近のタスク（1週間）だけリストを書き換える
    tasks = [t for t in tasks if today <= t.deadline <= next_w]
    # 直近の予定リンク
    links = [t.deadline.strftime('/todo/' + username + '/%Y/%m/%d') for t in tasks]

    return templates.TemplateResponse(
        'admin.html',
        {
            'request': request,
            'user': user,
            'tasks': tasks,
            'links': links,
            'calendar': cal
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
        error.append('同じユーザー名のユーザーが存在します')
    if password != password_tmp:
        error.append('入力したパスワードが一致しません')
    if pattern.match(username) is None:
        error.append('ユーザー名は4〜20文字の半角英数字にしてください')
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


# 予定詳細ページ
@app.get('/todo/{username}/{year}/{month}/{day}')
def read_detail(request: Request, username, year, month, day, credentials: HTTPBasicCredentials = Depends(security)):
    """
    URLのパターンは引数で取得できる
    Args:
        request (Request): URLでのリクエスト
        username (str): ユーザー名
        year (int): 年
        month (int): 月
        day (int): 日
    """

    # 認証okか
    username_tmp = basic_auth(credentials)

    # 他のユーザーが来た場合は弾く
    if username_tmp != username:
        return RedirectResponse('/')

    # ログインユーザー
    user = db.session.query(UserTable).filter(UserTable.username == username).first()
    # ログインユーザーの全タスクを取得
    user_all_tasks = db.session.query(TaskTable).filter(TaskTable.user_id == user.id).all()
    db.session.close()

    # 該当の日付と一致するものだけリストにする
    # 月と日は０埋め
    theday = '{}{}{}'.format(year, month.zfill(2), day.zfill(2))
    tasks = [t for t in user_all_tasks if t.deadline.strftime('%Y%m%d') == theday]

    return templates.TemplateResponse(
        'detail.html',
        {
            'request': request,
            'username': username,
            'tasks': tasks,
            'year': year,
            'month': month,
            'day': day
        }
    )


# 終了したことをPOST
@app.post('/done')
async def done(request: Request, credentials: HTTPBasicCredentials = Depends(security)):
    # 認証
    username = basic_auth(credentials)

    # ユーザー情報
    user = db.session.query(UserTable).filter(UserTable.username == username).first()

    # ログインユーザーのタスクを取得
    user_all_tasks = db.session.query(TaskTable).filter(TaskTable.user_id == user.id).all()

    # フォームで受け取ったタスクの終了判定を見て内容を変更する
    data = await request.form()
    # リストとして取得
    t_dones = data.getlist('done[]')

    for task in user_all_tasks:
        if str(task.id) in t_dones:
            task.done = True
        print(task)

    # update
    db.session.commit()
    db.session.close()

    # 管理者トップへリダイレクト
    return RedirectResponse('/admin')
