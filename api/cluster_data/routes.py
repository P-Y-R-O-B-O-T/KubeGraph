from fastapi import Depends
from cluster_data.methods import get_cluster_data, set_cluster_data
from cluster_data.schemas import ClusterDataRequest, ClusterData, ClusterDataUpload
from authentication.auth import get_current_active_user
from fastapi.responses import Response
from authentication.schemas import User
from typing import Annotated
from fastapi import APIRouter, status


CLUSTER_DATA_ROUTER = APIRouter(prefix="/cluster", tags=["cluster_data"])

CLUSTERS_DATA = {}

@CLUSTER_DATA_ROUTER.post("/data", status_code=status.HTTP_202_ACCEPTED)
def upload_cluster_data(
    data: Annotated[ClusterDataUpload, Depends()],
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    set_cluster_data(CLUSTERS_DATA, data)
    return Response(status_code=status.HTTP_202_ACCEPTED)

@CLUSTER_DATA_ROUTER.get("/data", response_model=ClusterData)
def fetch_cluster_data(
    cluster_data_request: Annotated[ClusterDataRequest, Depends()],
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return get_cluster_data(CLUSTERS_DATA, cluster_data_request)
