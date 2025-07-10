from state_runners.base.base_runner import BASE_RUNNER
from kubernetes import client


class StorageV1Api_RUNNER(BASE_RUNNER):
    def __init__(self, name) -> None:
        super().__init__(client.StorageV1Api, name)


class CSI_DRIVER_RUNNER(StorageV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("StorageV1Api_CSI_DRIVERS")

    def fetch_state(self, _):
        bookmark = self.REDIS_CONNECTOR.get_bookmark(_, self.NAME)
        # if bookmark == None : return []
        return self.WATCHERS[_].stream(
            self.CLIENTS[_].list_csi_driver,
            timeout_seconds=5,
            allow_watch_bookmarks=True,
            resource_version=bookmark,
        )


class CSI_NODE_RUNNER(StorageV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("StorageV1Api_CSI_NODES")

    def fetch_state(self, _):
        bookmark = self.REDIS_CONNECTOR.get_bookmark(_, self.NAME)
        # if bookmark == None : return []
        return self.WATCHERS[_].stream(
            self.CLIENTS[_].list_csi_node,
            timeout_seconds=5,
            allow_watch_bookmarks=True,
            resource_version=bookmark,
        )


class CSI_STORAGE_CAPACITY_RUNNER(StorageV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("StorageV1Api_CSI_STORAGE_CAPACITIES")

    def fetch_state(self, _):
        bookmark = self.REDIS_CONNECTOR.get_bookmark(_, self.NAME)
        # if bookmark == None : return []
        return self.WATCHERS[_].stream(
            self.CLIENTS[_].list_csi_storage_capacity_for_all_namespaces,
            timeout_seconds=5,
            allow_watch_bookmarks=True,
            resource_version=bookmark,
        )


class STORAGE_CLASS_RUNNER(StorageV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("StorageV1Api_STORAGE_CLASSES")

    def fetch_state(self, _):
        bookmark = self.REDIS_CONNECTOR.get_bookmark(_, self.NAME)
        # if bookmark == None : return []
        return self.WATCHERS[_].stream(
            self.CLIENTS[_].list_storage_class,
            timeout_seconds=5,
            allow_watch_bookmarks=True,
            resource_version=bookmark,
        )


class VOLUME_ATTACHMENT_RUNNER(StorageV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("StorageV1Api_VOLUME_ATTACHMENTS")

    def fetch_state(self, _):
        bookmark = self.REDIS_CONNECTOR.get_bookmark(_, self.NAME)
        # if bookmark == None : return []
        return self.WATCHERS[_].stream(
            self.CLIENTS[_].list_volume_attachment,
            timeout_seconds=5,
            allow_watch_bookmarks=True,
            resource_version=bookmark,
        )
