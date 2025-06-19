from state_runners.base.base_runner import BASE_RUNNER

from kubernetes import client,watch


class CustomObjectsApi_RUNNER(BASE_RUNNER):
    def __init__(self, name) -> None:
        super().__init__(client.CustomObjectsApi, name)


class CLUSTER_CUSTOM_OBJECT_RUNNER(CustomObjectsApi_RUNNER):
    def __init__(self) -> None:
        super().__init__("CustomObjectsApi_CLUSTER_CUSTOM_OBJECTS")

    def fetch_state(self, _):
        w=watch.Watch()
        return w.stream(self.CLIENTS[_].list_cluster_custom_object,timeout_seconds=0)


class CUSTOM_OBJECTS_RUNNER(CustomObjectsApi_RUNNER):
    def __init__(self) -> None:
        super().__init__("CustomObjectsApi_CUSTOM_OBJECTS")

    def fetch_state(self, _):
        w=watch.Watch()
        return w.stream(self.CLIENTS[_].list_custom_object_for_all_namespaces,timeout_seconds=0)

