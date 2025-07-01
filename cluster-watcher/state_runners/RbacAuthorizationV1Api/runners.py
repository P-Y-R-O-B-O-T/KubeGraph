from state_runners.base.base_runner import BASE_RUNNER
from kubernetes import client


class RbacAuthorizationV1Api_RUNNER(BASE_RUNNER):
    def __init__(self, name) -> None:
        super().__init__(client.RbacAuthorizationV1Api, name)


class CLUSTER_ROLE_RUNNER(RbacAuthorizationV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("RbacAuthorizationV1Api_CLUSTER_ROLES")

    def fetch_state(self, _):
        return self.WATCHERS[_].stream(
            self.CLIENTS[_].list_cluster_role,
            timeout_seconds=5,
            allow_watch_bookmarks=True,
            resource_version=self.LATEST_RESOURCE_VERSION,
        )


class CLUSTER_ROLE_BINDINGS_RUNNER(RbacAuthorizationV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("RbacAuthorizationV1Api_CLUSTER_ROLE_BINDINGS")

    def fetch_state(self, _):
        return self.WATCHERS[_].stream(
            self.CLIENTS[_].list_cluster_role_binding,
            timeout_seconds=5,
            allow_watch_bookmarks=True,
            resource_version=self.LATEST_RESOURCE_VERSION,
        )


class ROLE_BINDING_RUNNER(RbacAuthorizationV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("RbacAuthorizationV1Api_ROLE_BINDINGS")

    def fetch_state(self, _):
        return self.WATCHERS[_].stream(
            self.CLIENTS[_].list_role_binding_for_all_namespaces,
            timeout_seconds=5,
            allow_watch_bookmarks=True,
            resource_version=self.LATEST_RESOURCE_VERSION,
        )


class ROLE_RUNNER(RbacAuthorizationV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("RbacAuthorizationV1Api_ROLES")

    def fetch_state(self, _):
        return self.WATCHERS[_].stream(
            self.CLIENTS[_].list_role_for_all_namespaces,
            timeout_seconds=5,
            allow_watch_bookmarks=True,
            resource_version=self.LATEST_RESOURCE_VERSION,
        )
