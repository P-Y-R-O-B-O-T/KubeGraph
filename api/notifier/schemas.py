
from pydantic import BaseModel,Field
from typing import Optional,Dict,Literal
from datetime import datetime

class NotifyEvent(BaseModel):
    name:str=Field(...,description="The name of the event")
    namespace:Optional[str]=Field(None,description="The namespace of the event")
    target_type:str=Field(...,description="The type of the target")
    target_id:str=Field(...,description="The id of the target")
    status:Literal["added","updated","deleted"]=Field(...,description="The status")
    timestamp:datetime=Field(default_factory=datetime.now,description="timestamp")

class EventData(BaseModel):
    event_type:str=Field(...)
    event_id:str=Field(...)
    target_type:str=Field(...) # this can pod or service or deployment
    resource_type:str=Field(...)
    status:Literal["added","updated","deleted"]
    cluster_name:str=Field(...)
    timestamp:datetime=Field(default_factory=datetime.now)


