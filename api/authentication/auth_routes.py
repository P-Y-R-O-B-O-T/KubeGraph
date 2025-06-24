from fastapi import Depends
from authentication.schemas import Token
from authentication.auth import get_auth_token
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from fastapi import APIRouter


AUTH_ROUTER = APIRouter(prefix="/auth", tags=["auth"])


@AUTH_ROUTER.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    return get_auth_token(form_data)
