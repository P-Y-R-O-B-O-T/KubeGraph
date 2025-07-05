from pydantic import BaseModel
from typing import Any, Dict


class ClusterDataUpload(BaseModel):
    cluster_name: str
    resource_type: str
    cluster_data: Dict


class ObjectDataUpload(BaseModel):
    cluster_name: str
    resource_type: str
    resource_uid: str
    event_type: str
    object_data: Dict


class ClusterData(BaseModel):
    cluster_name: str
    cluster_data: Dict


class ClusterDataRequest(BaseModel):
    cluster_name: str
