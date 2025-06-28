

from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Dict,Optional,Any
import json

@dataclass

class MonitoringMessage:
    cluster_name:str
    resource_name:str
    namespace:Optional[str] 
    action:str ## Created Modified Deleted.
    timestamp:datetime
    data:Dict[str,Any]



    def to_json(self)->str:
        def default(o):
            if isinstance(o, datetime):
                return o.isoformat()
            return str(o)

        return json.dumps(asdict(self), default=default)

    @classmethod

    def from_json(cls,json_str:str)->'MonitoringMessage':
        data=json.loads(json_str)
        data['timestamp']=datetime.fromisoformat(data['timestamp'])
        return cls(**data)
        
    def to_dict(self):
        return {
            "cluster_name": self.cluster_name,
            "resource_name": self.resource_name,
            "namespace": self.namespace,
            "action": self.action,
            "timestamp": self.timestamp.isoformat() if hasattr(self.timestamp, "isoformat") else self.timestamp,
            "data": self.data,
        }
