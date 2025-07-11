from state_runners.base.base_runner import BASE_RUNNER
from kubernetes import client


class AppsV1Api_RUNNER(BASE_RUNNER):
    def __init__(self, name) -> None:
        super().__init__(client.AppsV1Api, name)


# ❌ Watch not supported for ControllerRevision
class CONTROLLER_VERSION_RUNNER(AppsV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("AppsV1Api_CONTROLLER_VERSIONS")

    def fetch_state(self, _):
        return self.CLIENTS[_].list_controller_revision_for_all_namespaces(
            **{"timeout_seconds": 20, "_request_timeout": 20}
        )


class DAEMONSET_RUNNER(AppsV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("AppsV1Api_DAEMONSETS")

    def fetch_state(self, _):
        bookmark = self.REDIS_CONNECTOR.get_bookmark(_, self.NAME)
        # if bookmark == None : return []
        return self.WATCHERS[_].stream(
            self.CLIENTS[_].list_daemon_set_for_all_namespaces,
            timeout_seconds=5,
            allow_watch_bookmarks=True,
            resource_version=bookmark,
        )


class DEPLOYMENT_RUNNER(AppsV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("AppsV1Api_DEPLOYMENTS")

    def fetch_state(self, _):
        bookmark = self.REDIS_CONNECTOR.get_bookmark(_, self.NAME)
        # if bookmark == None : return []
        return self.WATCHERS[_].stream(
            self.CLIENTS[_].list_deployment_for_all_namespaces,
            timeout_seconds=5,
            allow_watch_bookmarks=True,
            resource_version=bookmark,
        )


class REPLICASET_RUNNER(AppsV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("AppsV1Api_REPLICASETS")

    def fetch_state(self, _):
        bookmark = self.REDIS_CONNECTOR.get_bookmark(_, self.NAME)
        # if bookmark == None : return []
        return self.WATCHERS[_].stream(
            self.CLIENTS[_].list_replica_set_for_all_namespaces,
            timeout_seconds=5,
            allow_watch_bookmarks=True,
            resource_version=bookmark,
        )


class STATEFULSET_RUNNER(AppsV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("AppsV1Api_STATEFULSETS")

    def fetch_state(self, _):
        bookmark = self.REDIS_CONNECTOR.get_bookmark(_, self.NAME)
        # if bookmark == None : return []
        return self.WATCHERS[_].stream(
            self.CLIENTS[_].list_stateful_set_for_all_namespaces,
            timeout_seconds=5,
            allow_watch_bookmarks=True,
            resource_version=bookmark,
        )
