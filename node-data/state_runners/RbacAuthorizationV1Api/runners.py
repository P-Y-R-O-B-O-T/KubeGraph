from state_runners.base.base_runner import BASE_RUNNER
from kubernetes import client


class RbacAuthorizationV1Api_RUNNER(BASE_RUNNER):
    def __init__(self, name) -> None:
        super().__init__(client.RbacAuthorizationV1Api, name)


class CLUSTER_ROLE_RUNNER(RbacAuthorizationV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("RbacAuthorizationV1Api_CLUSTER_ROLES")

    def get_object_data(self, _):
        return {}


class CLUSTER_ROLE_BINDINGS_RUNNER(RbacAuthorizationV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("RbacAuthorizationV1Api_CLUSTER_ROLE_BINDINGS")

    def get_object_data(self, _):
        return {}


class ROLE_BINDING_RUNNER(RbacAuthorizationV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("RbacAuthorizationV1Api_ROLE_BINDINGS")

    def get_object_data(self, _):
        return {}


class ROLE_RUNNER(RbacAuthorizationV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("RbacAuthorizationV1Api_ROLES")

    def get_object_data(self, _):
        return {}
