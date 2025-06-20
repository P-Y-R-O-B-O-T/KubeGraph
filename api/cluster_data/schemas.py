# cluster_data/schemas.py

from pydantic import BaseModel
from typing import Any, Dict

class ClusterDataType(BaseModel):
    username: str
    content: Dict
