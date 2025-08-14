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

    

    
    def get_metadata(self,data:dict)->dict:
        
        
        if not data:
            raise ValueError("Data must not be empty")
        
        
        object_metadata=data.get("metadata",{})

         

        return {
        "generation": object_metadata["generation"],
        "name": object_metadata["name"],
        "namespace": object_metadata["namespace"],
        "uid": object_metadata["uid"],
        "resource_version": object_metadata["resourceVersion"],
        "labels": object_metadata["labels"],
        "annotations": object_metadata["annotations"],
        "owner_references": object_metadata["ownerReferences"],
        "creation_timestamp": object_metadata["creationTimestamp"],
        "deletion_timestamp": object_metadata.get("deletionTimestamp"),
        }

   
    @abstractmethod
    def get_data(self, _):
        raise NotImplementedError("Subclasses must implement fetch_state")
