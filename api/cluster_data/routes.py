from fastapi import Depends
from cluster_data.download import get_cluster_data
from cluster_data.schemas import ClusterDataRequest, ClusterData, ClusterDataUpload
from authentication.auth import get_current_active_user
from authentication.schemas import User
from cluster_data.upload import set_cluster_data
from typing import Annotated
from fastapi import APIRouter


CLUSTER_DATA_ROUTER = APIRouter(prefix="/cluster", tags=["cluster_data"])

CLUSTERS_DATA = {}

@CLUSTER_DATA_ROUTER.post("/data", response_model=ClusterData)
def upload_cluster_data(
    data: Annotated[ClusterDataUpload, Depends()],
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    set_cluster_data(CLUSTERS_DATA, data)
    return get_cluster_data(CLUSTERS_DATA, ClusterDataRequest(cluster_name=data.cluster_name))

@CLUSTER_DATA_ROUTER.get("/data", response_model=ClusterData)
def fetch_cluster_data(
    cluster_data_request: Annotated[ClusterDataRequest, Depends()],
    current_user: Annotated[User, Depends(get_current_active_user)]
):
    return get_cluster_data(CLUSTERS_DATA, cluster_data_request)
