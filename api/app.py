from fastapi import FastAPI
from authentication.auth_routes import AUTH_ROUTER
from cluster_data.routes import CLUSTER_DATA_ROUTER

APP = FastAPI(root_path="/api")

APP.include_router(AUTH_ROUTER)
APP.include_router(CLUSTER_DATA_ROUTER)
