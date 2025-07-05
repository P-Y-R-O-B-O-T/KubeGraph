from fastapi import Body, Depends
from cluster_data.methods import get_cluster_data, set_cluster_data, update_cluster_objects
from cluster_data.schemas import (
    ClusterDataRequest,
    ClusterData,
    ClusterDataUpload,
    ObjectDataUpload,
)
from authentication.auth import get_current_active_user
from fastapi.responses import Response
from authentication.schemas import User
from typing import Annotated
from fastapi import APIRouter, status


CLUSTER_DATA_ROUTER = APIRouter(prefix="/cluster", tags=["cluster_data"])

CLUSTERS_DATA = {}


@CLUSTER_DATA_ROUTER.post("/data", status_code=status.HTTP_202_ACCEPTED)
async def upload_cluster_data(
    data: Annotated[ClusterDataUpload, Body()],
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    set_cluster_data(CLUSTERS_DATA, data)
    return Response(status_code=status.HTTP_202_ACCEPTED)


@CLUSTER_DATA_ROUTER.get("/data", response_model=ClusterData)
async def fetch_cluster_data(
    cluster_data_request: Annotated[ClusterDataRequest, Depends()],
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return get_cluster_data(CLUSTERS_DATA, cluster_data_request)


@CLUSTER_DATA_ROUTER.put("/data", status_code=status.HTTP_202_ACCEPTED)
async def update_cluster_data(
    data: Annotated[ObjectDataUpload, Body()],
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    update_cluster_objects(CLUSTERS_DATA, data)
    return Response(status_code=status.HTTP_202_ACCEPTED)
