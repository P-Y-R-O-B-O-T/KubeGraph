
import datetime
from pydoc import describe
from typing import Any, Dict, List,Optional,TypedDict
from pydantic import BaseModel,Field


class ObjecteMetadata(BaseModel):
    ## Every object kind has metadata not resouce, 
    object_type:str=Field(...,description="The type of the resource")
    generation:int=Field(...,description="generation")
    name:str=Field(...,description="name of the resource")
    namespace:Optional[str]=Field(None,descrption="namespace of the resource")
    uid:str=Field(...)
    resource_version:str=Field(...)
    labels:Dict[str,str]=Field(...,description="labels of resouce")
    annotations:Dict[str,str]=Field(...,description="annnotation of resource")
    owner_references:List[Dict[str,Any]]=Field(...,description="owner references")
    creation_timestamp:datetime=Field(...,description="creation timestamp")
    deletion_timestamp:Optional[datetime]=Field(None,description="deletion timestamp")
    

