from state_runners.base.base_runner import BASE_RUNNER
from kubernetes import client


class CoreV1Api_RUNNER(BASE_RUNNER):
    def __init__(self, name) -> None:
        super().__init__(client.CoreV1Api, name)


class POD_RUNNER(CoreV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("CoreV1Api_PODS")

    def fetch_state(self, _):
        bookmark = self.REDIS_CONNECTOR.get_bookmark(_, self.NAME)
        # if bookmark == None : return []
        return self.WATCHERS[_].stream(
            self.CLIENTS[_].list_pod_for_all_namespaces,
            timeout_seconds=5,
            allow_watch_bookmarks=True,
            resource_version=bookmark,
        )


class NAMESPACE_RUNNER(CoreV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("CoreV1Api_NAMESPACES")

    def fetch_state(self, _):
        bookmark = self.REDIS_CONNECTOR.get_bookmark(_, self.NAME)
        # if bookmark == None : return []
        return self.WATCHERS[_].stream(
            self.CLIENTS[_].list_namespace,
            timeout_seconds=5,
            allow_watch_bookmarks=True,
            resource_version=bookmark,
        )


class CONFIGMAP_RUNNER(CoreV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("CoreV1Api_CONFIGMAPS")

    def fetch_state(self, _):
        bookmark = self.REDIS_CONNECTOR.get_bookmark(_, self.NAME)
        # if bookmark == None : return []
        return self.WATCHERS[_].stream(
            self.CLIENTS[_].list_config_map_for_all_namespaces,
            timeout_seconds=5,
            allow_watch_bookmarks=True,
            resource_version=bookmark,
        )


class ENDPOINT_RUNNER(CoreV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("CoreV1Api_ENDPOINTS")

    def fetch_state(self, _):
        bookmark = self.REDIS_CONNECTOR.get_bookmark(_, self.NAME)
        # if bookmark == None : return []
        return self.WATCHERS[_].stream(
            self.CLIENTS[_].list_endpoints_for_all_namespaces,
            timeout_seconds=5,
            allow_watch_bookmarks=True,
            resource_version=bookmark,
        )


class EVENT_RUNNER(CoreV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("CoreV1Api_EVENTS")

    def fetch_state(self, _):
        bookmark = self.REDIS_CONNECTOR.get_bookmark(_, self.NAME)
        # if bookmark == None : return []
        return self.WATCHERS[_].stream(
            self.CLIENTS[_].list_event_for_all_namespaces,
            timeout_seconds=5,
            send_initial_events=True,
            resource_version_match="NotOlderThan",
            resource_version=bookmark,
        )


class LIMIT_RANGE_RUNNER(CoreV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("CoreV1Api_LIMIT_RANGES")

    def fetch_state(self, _):
        bookmark = self.REDIS_CONNECTOR.get_bookmark(_, self.NAME)
        # if bookmark == None : return []
        return self.WATCHERS[_].stream(
            self.CLIENTS[_].list_limit_range_for_all_namespaces,
            timeout_seconds=5,
            allow_watch_bookmarks=True,
            resource_version=bookmark,
        )


class NODE_RUNNER(CoreV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("CoreV1Api_NODES")

    def fetch_state(self, _):
        bookmark = self.REDIS_CONNECTOR.get_bookmark(_, self.NAME)
        # if bookmark == None : return []
        return self.WATCHERS[_].stream(
            self.CLIENTS[_].list_node,
            timeout_seconds=5,
            allow_watch_bookmarks=True,
            resource_version=bookmark,
        )


class PV_RUNNER(CoreV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("CoreV1Api_PVS")

    def fetch_state(self, _):
        bookmark = self.REDIS_CONNECTOR.get_bookmark(_, self.NAME)
        # if bookmark == None : return []
        return self.WATCHERS[_].stream(
            self.CLIENTS[_].list_persistent_volume,
            timeout_seconds=5,
            allow_watch_bookmarks=True,
            resource_version=bookmark,
        )


class PVC_RUNNER(CoreV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("CoreV1Api_PVCS")

    def fetch_state(self, _):
        bookmark = self.REDIS_CONNECTOR.get_bookmark(_, self.NAME)
        # if bookmark == None : return []
        return self.WATCHERS[_].stream(
            self.CLIENTS[_].list_persistent_volume_claim_for_all_namespaces,
            timeout_seconds=5,
            allow_watch_bookmarks=True,
            resource_version=bookmark,
        )


class POD_TEMPLATE_RUNNER(CoreV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("CoreV1Api_POD_TEMPLATES")

    def fetch_state(self, _):
        bookmark = self.REDIS_CONNECTOR.get_bookmark(_, self.NAME)
        # if bookmark == None : return []
        return self.WATCHERS[_].stream(
            self.CLIENTS[_].list_pod_template_for_all_namespaces,
            timeout_seconds=5,
            allow_watch_bookmarks=True,
            resource_version=bookmark,
        )


class REPLICATION_CONTROLLER_RUNNER(CoreV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("CoreV1Api_REPLICATION_CONTROLLERS")

    def fetch_state(self, _):
        bookmark = self.REDIS_CONNECTOR.get_bookmark(_, self.NAME)
        # if bookmark == None : return []
        return self.WATCHERS[_].stream(
            self.CLIENTS[_].list_replication_controller_for_all_namespaces,
            timeout_seconds=5,
            allow_watch_bookmarks=True,
            resource_version=bookmark,
        )


class RESOURCE_QUOTA_RUNNER(CoreV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("CoreV1Api_RESOURCE_QUOTAS")

    def fetch_state(self, _):
        bookmark = self.REDIS_CONNECTOR.get_bookmark(_, self.NAME)
        # if bookmark == None : return []
        return self.WATCHERS[_].stream(
            self.CLIENTS[_].list_resource_quota_for_all_namespaces,
            timeout_seconds=5,
            allow_watch_bookmarks=True,
            resource_version=bookmark,
        )


class SECRET_RUNNER(CoreV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("CoreV1Api_SECRETS")

    def fetch_state(self, _):
        bookmark = self.REDIS_CONNECTOR.get_bookmark(_, self.NAME)
        # if bookmark == None : return []
        return self.WATCHERS[_].stream(
            self.CLIENTS[_].list_secret_for_all_namespaces,
            timeout_seconds=5,
            allow_watch_bookmarks=True,
            resource_version=bookmark,
        )


class SERVICE_ACCOUNT_RUNNER(CoreV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("CoreV1Api_SERVICE_ACCOUNTS")

    def fetch_state(self, _):
        bookmark = self.REDIS_CONNECTOR.get_bookmark(_, self.NAME)
        # if bookmark == None : return []
        return self.WATCHERS[_].stream(
            self.CLIENTS[_].list_service_account_for_all_namespaces,
            timeout_seconds=5,
            allow_watch_bookmarks=True,
            resource_version=bookmark,
        )


class SERVICE_RUNNER(CoreV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("CoreV1Api_SERVICES")

    def fetch_state(self, _):
        bookmark = self.REDIS_CONNECTOR.get_bookmark(_, self.NAME)
        # if bookmark == None : return []
        return self.WATCHERS[_].stream(
            self.CLIENTS[_].list_service_for_all_namespaces,
            timeout_seconds=5,
            allow_watch_bookmarks=True,
            resource_version=bookmark,
        )
