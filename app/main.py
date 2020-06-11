from fastapi import FastAPI
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

app = FastAPI(
    title='FastAPIで作成するTODOアプリ',
    description='シンプルなTODOアプリです',
    version='0.9 beta'
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
    return templates.TemplateResponse(
        'admin.html',
        {
            'request': request,
            'username': 'admin'
        }
    )