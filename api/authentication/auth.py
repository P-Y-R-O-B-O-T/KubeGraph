import os
from datetime import datetime, timedelta, timezone
import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm
from authentication.database import UsersDB
from authentication.schemas import User, UserInDB, Token
from authentication.errors import INCORRECT_CREDENTIALS, ILLEGAL_EXPIRED_TOKEN

PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("API_AUTH_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="/api/auth/token")
USERS_DB = UsersDB("USERS", "USERS")


def get_auth_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    pass
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(**INCORRECT_CREDENTIALS)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return PWD_CONTEXT.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return PWD_CONTEXT.hash(password)


def authenticate_user(username: str, password: str) -> UserInDB | None:
    user = USERS_DB.get_user(username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> str | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
        return username
    except InvalidTokenError:
        return None


async def get_current_user(
    token: Annotated[str, Depends(OAUTH2_SCHEME)],
) -> User:
    credentials_exception = HTTPException(**ILLEGAL_EXPIRED_TOKEN)
    username = decode_token(token)
    if username is None:
        raise credentials_exception

    user = USERS_DB.get_user(username=username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
