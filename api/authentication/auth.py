# auth.py
import os
from datetime import datetime, timedelta, timezone

import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from dotenv import load_dotenv
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from authentication.fake_database import fake_users_db
from authentication.database import Database
from authentication.schemas import User, UserInDB

load_dotenv()

PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "dfgfgfgbdfkbvkfbvkkx"  # os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="token")
USERS_DB = Database()


class AuthService:
    def __init__(self) -> None:
        # self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        # self.SECRET_KEY = "dfgfgfgbdfkbvkfbvkkx" #os.getenv("SECRET_KEY")
        # self.ALGORITHM = "HS256"
        # self.ACCESS_TOKEN_EXPIRE_MINUTES = 30
        # self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
        pass

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return PWD_CONTEXT.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return PWD_CONTEXT.hash(password)

    # def get_user(self, db: dict, username: str) -> UserInDB | None:
    #     if username in db:
    #         user_dict = db[username]
    #         return UserInDB(**user_dict)
    #     return None
    #
    # def get_user_db(self, username: str) -> UserInDB | None:
    #     user = USERS_DB.get_user(username)
    #     if user :
    #         return user

    def authenticate_user(self, username: str, password: str) -> UserInDB | None:
        # user = self.get_user_db(username)
        user = USERS_DB.get_user(username)
        if not user or not self.verify_password(password, user.hashed_password):
            return None
        return user

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def decode_token(self, token: str) -> str | None:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str | None = payload.get("sub")
            return username
        except InvalidTokenError:
            return None

    async def get_current_user(
        self,
        token: Annotated[str, Depends(OAUTH2_SCHEME)],
        # db: Annotated[dict, Depends(get_db)]
    ) -> User:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        username = self.decode_token(token)
        if username is None:
            raise credentials_exception

        user = USERS_DB.get_user(username=username)
        if user is None:
            raise credentials_exception
        return user

    async def get_current_active_user(
        self,
        current_user: Annotated[User, Depends(get_current_user)],
    ):
        if current_user.disabled:
            raise HTTPException(status_code=400, detail="Inactive user")
        return current_user

    def token_expire_minutes(self) -> int:
        return ACCESS_TOKEN_EXPIRE_MINUTES
