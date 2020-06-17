import hashlib
import db
from models import UserTable
from starlette.status import HTTP_401_UNAUTHORIZED
from fastapi import HTTPException


def basic_auth(credentials):
    """
    Basic認証
    """

    # リクエスト情報
    username = credentials.username
    password = hashlib.md5(credentials.password.encode()).hexdigest()
    # UserTableからユーザ名が一致する情報を取得
    user = db.session.query(UserTable).filter(UserTable.username == username).first()
    db.session.close()

    if user is None or user.password != password:
        error = 'ユーザ名かパスワードが間違っています'
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail=error,
            headers={"WWW-Authenticate": "Basic"},
        )

    return username
