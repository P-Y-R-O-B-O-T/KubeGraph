from fastapi import Depends
from authentication.schemas import Token
from authentication.auth import AuthService
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from fastapi import APIRouter

class AuthRoutes:
    def __init__(self) -> None:
        self.AUTH_MECHANISM = AuthService()
        self.ROUTER = APIRouter(prefix="/auth", tags=["auth"])

        self.ROUTER.post("/token", response_model=Token)(self.login_for_access_token)


    async def login_for_access_token(
        self,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    ):
        return self.AUTH_MECHANISM.get_auth_token(form_data)
