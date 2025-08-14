from state_runners.base.base_runner import BASE_RUNNER

from kubernetes import client


class CustomObjectsApi_RUNNER(BASE_RUNNER):
    def __init__(self, name) -> None:
        super().__init__(client.CustomObjectsApi, name)


class CLUSTER_CUSTOM_OBJECT_RUNNER(CustomObjectsApi_RUNNER):
    def __init__(self) -> None:
        super().__init__("CustomObjectsApi_CLUSTER_CUSTOM_OBJECTS")

    def get_object_data(self, _):
        # ⚠️ NEEDS TO BE HEAVILY MODIFIED
        return {}


class CUSTOM_OBJECTS_RUNNER(CustomObjectsApi_RUNNER):
    def __init__(self) -> None:
        super().__init__("CustomObjectsApi_CUSTOM_OBJECTS")

    def get_object_data(self, _):
        # ⚠️ NEEDS TO BE HEAVILY MODIFIED
        return {}
