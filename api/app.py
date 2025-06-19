from fastapi import FastAPI
from authentication.auth_routes import AuthRoutes

APP = FastAPI(root_path="/api")

AUTH_ROUTES = AuthRoutes()

APP.include_router(AUTH_ROUTES.ROUTER)
