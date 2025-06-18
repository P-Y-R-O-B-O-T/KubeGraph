from fastapi import FastAPI
from authentication.auth_routes import AuthRoutes

APP = FastAPI()

AUTH_ROUTES = AuthRoutes()

APP.include_router(AUTH_ROUTES.ROUTER)
