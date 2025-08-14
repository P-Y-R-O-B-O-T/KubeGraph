from state_runners.base.base_runner import BASE_RUNNER
from kubernetes import client


class StorageV1Api_RUNNER(BASE_RUNNER):
    def __init__(self, name) -> None:
        super().__init__(client.StorageV1Api, name)


class CSI_DRIVER_RUNNER(StorageV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("StorageV1Api_CSI_DRIVERS")

    def get_object_data(self, _):
        return {}


class CSI_NODE_RUNNER(StorageV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("StorageV1Api_CSI_NODES")

    def get_object_data(self, _):
        return {}


class CSI_STORAGE_CAPACITY_RUNNER(StorageV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("StorageV1Api_CSI_STORAGE_CAPACITIES")

    def get_object_data(self, _):
        return {}


class STORAGE_CLASS_RUNNER(StorageV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("StorageV1Api_STORAGE_CLASSES")

    def get_object_data(self, _):
        return {}


class VOLUME_ATTACHMENT_RUNNER(StorageV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("StorageV1Api_VOLUME_ATTACHMENTS")

    def get_object_data(self, _):
        return {}
