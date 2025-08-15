from abc import abstractmethod
from rich.console import Console
from datetime import datetime
import traceback


class BASE_RUNNER:
    def __init__(self, name: str) -> None:
        self.RICH_CONSOLE = Console(
            force_terminal=True,
            color_system="truecolor",
            log_path=False,
            safe_box=False,
        )
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
        "creation_timestamp": object_metadata["creationTimestamp"],
        "labels": object_metadata["labels"],
        "annotations": object_metadata["annotations"],
        "owner_references": object_metadata.get("ownerReferences"),
        "deletion_timestamp": object_metadata.get("deletionTimestamp"),
        }
   
    @abstractmethod
    def get_data(self, _):
        raise NotImplementedError("Subclasses must implement get_object_data")
