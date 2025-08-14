from abc import abstractmethod

from email.policy import default
from pydoc import safeimport
from typing import Any,List
from rich.console import Console
import asyncio
import os
import sys
import time
from datetime import datetime
import traceback
from schemas import ObjecteMetadata

from redis_connector.redis_connector import REDIS_CONNECTOR


class BASE_RUNNER:
    def __init__(self, api_object_class, name: str) -> None:
        self.RICH_CONSOLE = Console(
            force_terminal=True,
            color_system="truecolor",
            log_path=False,
            safe_box=False,
        )

        self.API_OBJECT_CLASS = api_object_class
        self.REDIS_CONNECTOR = REDIS_CONNECTOR()
        self.NAME = name

    def get_int_data(self, data: dict, key: str, default: int = 0) -> int:
        value = data.get(key, default)
        try:
            return int(value) if value is not None else default
        except (ValueError, TypeError):
            return default
    
    def get_dict_data(data: dict, key: str) ->dict:

        value = data.get(key, {})
        return value if isinstance(value, dict) else {}


    def get_list_data(data: dict, key: str) -> List[Any]:
    
        value = data.get(key, [])
        return value if isinstance(value, list) else []

    
    def get_metadata(self,object_type:str,data:dict)->ObjecteMetadata:
        
        if not object_type or not object_type.strip():
            raise ValueError("Object type is required")
        if not data:
            raise ValueError("Data must not be empty")
        
        
        object_metadata=data.get("metadata",{})

        if not object_metadata:
            raise KeyError("Resource missing 'metadata' fieldss") 

        return ObjecteMetadata(
        resource_type=object_type.strip(),
        generation=self.get_int_data(object_metadata, "generation", default=0),
        name=object_metadata["name"],
        namespace=object_metadata.get("namespace"),
        uid=object_metadata["uid"],
        resource_version=object_metadata["resourceVersion"],
        labels=self.get_dict_data(object_metadata, "labels"),
        annotations=self.get_dict_data(object_metadata, "annotations"),
        owner_references=self.get_list_data(object_metadata, "ownerReferences"),
        creation_timestamp=object_metadata["creationTimestamp"],
        deletion_timestamp=object_metadata.get("deletionTimestamp"),
    )

   
    @abstractmethod
    def get_data(self, _):
        raise NotImplementedError("Subclasses must implement fetch_state")
