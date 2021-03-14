from app.database import SessionLocal
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta

from sqlalchemy.orm.session import Session
from jose import jwt

from .models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def authenticate(db: Session, username: str, password: str):
    # """パスワード認証し、userを返却"""
    user = db.query(User).filter(User.email == username).first()
    if user.hashed_password != password + "notreallyhashed":
        raise HTTPException(status_code=401, detail='パスワード不一致')
    return user


def create_tokens(db: Session, user_id: int):
    # """パスワード認証を行い、トークンを生成"""
    # ペイロード作成
    access_payload = {
        'token_type': 'access_token',
        'exp': datetime.utcnow() + timedelta(minutes=60),
        'user_id': user_id,
    }
    refresh_payload = {
        'token_type': 'refresh_token',
        'exp': datetime.utcnow() + timedelta(days=90),
        'user_id': user_id,
    }

    # トークン作成（本来は'SECRET_KEY123'はもっと複雑にする）
    access_token = jwt.encode(access_payload, 'SECRET_KEY123', algorithm='HS256')
    refresh_token = jwt.encode(refresh_payload, 'SECRET_KEY123', algorithm='HS256')

    # DBにリフレッシュトークンを保存
    db_user = db.query(User).filter(User.id == int(user_id)).first()
    db_user.refresh_token = refresh_token
    db.commit()
    db.refresh(db_user)
    # User.update(refresh_token=refresh_token).where(User.id == user_id).execute()

    return {'access_token': access_token, 'refresh_token': refresh_token, 'token_type': 'bearer'}


def get_current_user_from_token(token: str, token_type: str):
    # """tokenからユーザーを取得"""
    # トークンをデコードしてペイロードを取得。有効期限と署名は自動で検証される。
    payload = jwt.decode(token, 'SECRET_KEY123', algorithms=['HS256'])

    # トークンタイプが一致することを確認
    if payload['token_type'] != token_type:
        raise HTTPException(status_code=401, detail=f'トークンタイプ不一致')

    # DBからユーザーを取得
    # user = User.get_by_id(payload['user_id'])
    db = SessionLocal()
    user = db.query(User).filter(User.id == int(payload['user_id'])).first()

    # リフレッシュトークンの場合、受け取ったものとDBに保存されているものが一致するか確認
    if token_type == 'refresh_token' and user.refresh_token != token:
        print(user.refresh_token, '¥n', token)
        raise HTTPException(status_code=401, detail='リフレッシュトークン不一致')

    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    # """アクセストークンからログイン中のユーザーを取得"""
    return get_current_user_from_token(token, 'access_token')


async def get_current_user_with_refresh_token(token: str = Depends(oauth2_scheme)):
    # """リフレッシュトークンからログイン中のユーザーを取得"""
    return get_current_user_from_token(token, 'refresh_token')