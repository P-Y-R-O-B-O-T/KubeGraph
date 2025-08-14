from state_runners.base.base_runner import BASE_RUNNER
from kubernetes import client


class CoreV1Api_RUNNER(BASE_RUNNER):
    def __init__(self, name) -> None:
        super().__init__(client.CoreV1Api, name)


class POD_RUNNER(CoreV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("CoreV1Api_PODS")

    def get_object_data(self, _):
        return {}


class NAMESPACE_RUNNER(CoreV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("CoreV1Api_NAMESPACES")

    def get_object_data(self, _):
        return {}


class CONFIGMAP_RUNNER(CoreV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("CoreV1Api_CONFIGMAPS")

    def get_object_data(self, _):
        return {}


class ENDPOINT_RUNNER(CoreV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("CoreV1Api_ENDPOINTS")

    def get_object_data(self, _):
        return {}


class EVENT_RUNNER(CoreV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("CoreV1Api_EVENTS")

    def get_object_data(self, _):
        return {}


class LIMIT_RANGE_RUNNER(CoreV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("CoreV1Api_LIMIT_RANGES")

    def get_object_data(self, _):
        return {}


class NODE_RUNNER(CoreV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("CoreV1Api_NODES")

    def get_object_data(self, _):
        return {}


class PV_RUNNER(CoreV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("CoreV1Api_PVS")

    def get_object_data(self, _):
        return {}


class PVC_RUNNER(CoreV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("CoreV1Api_PVCS")

    def get_object_data(self, _):
        return {}


class POD_TEMPLATE_RUNNER(CoreV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("CoreV1Api_POD_TEMPLATES")

    def get_object_data(self, _):
        return {}


class REPLICATION_CONTROLLER_RUNNER(CoreV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("CoreV1Api_REPLICATION_CONTROLLERS")

    def get_object_data(self, _):
        return {}


class RESOURCE_QUOTA_RUNNER(CoreV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("CoreV1Api_RESOURCE_QUOTAS")

    def get_object_data(self, _):
        return {}


class SECRET_RUNNER(CoreV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("CoreV1Api_SECRETS")

    def get_object_data(self, _):
        return {}


class SERVICE_ACCOUNT_RUNNER(CoreV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("CoreV1Api_SERVICE_ACCOUNTS")

    def get_object_data(self, _):
        return {}


class SERVICE_RUNNER(CoreV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("CoreV1Api_SERVICES")

    def get_object_data(self, _):
        return {}
