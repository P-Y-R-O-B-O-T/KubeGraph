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
from fake_database import fake_users_db
from schemas import User, UserInDB

load_dotenv()

class AuthService:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    SECRET_KEY = os.getenv("SECRET_KEY")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def get_user(self, db: dict, username: str) -> UserInDB | None:
        if username in db:
            user_dict = db[username]
            return UserInDB(**user_dict)
        return None

    def authenticate_user(self, db: dict, username: str, password: str) -> UserInDB | None:
        user = self.get_user(db, username)
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
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    def decode_token(self, token: str) -> str | None:
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            username: str | None = payload.get("sub")
            return username
        except InvalidTokenError:
            return None
    
    
    def get_db(self,):
        """It's a reusable helper function that opens a connection to the database."""
        return fake_users_db

    async def get_current_user(
        self,
        token: Annotated[str, Depends(oauth2_scheme)],
        db: Annotated[dict, Depends(get_db)]
    ) -> User:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        username = auth_service.decode_token(token)
        if username is None:
            raise credentials_exception
        
        user = auth_service.get_user(db, username=username)
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