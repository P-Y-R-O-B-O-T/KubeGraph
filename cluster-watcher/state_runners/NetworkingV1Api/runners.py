from state_runners.base.base_runner import BASE_RUNNER
from kubernetes import client


class NetworkingV1Api_RUNNER(BASE_RUNNER):
    def __init__(self, name) -> None:
        super().__init__(client.NetworkingV1Api, name)


class INGRESS_CLASS_RUNNER(NetworkingV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("NetworkingV1Api_INGRESS_CLASSES")

    def fetch_state(self, _):
        bookmark = self.REDIS_CONNECTOR.get_bookmark(_, self.NAME)
        # if bookmark == None : return []
        return self.WATCHERS[_].stream(
            self.CLIENTS[_].list_ingress_class,
            timeout_seconds=5,
            allow_watch_bookmarks=True,
            resource_version=bookmark,
        )


class INGRESS_RUNNER(NetworkingV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("NetworkingV1Api_INGRESSES")

    def fetch_state(self, _):
        bookmark = self.REDIS_CONNECTOR.get_bookmark(_, self.NAME)
        # if bookmark == None : return []
        return self.WATCHERS[_].stream(
            self.CLIENTS[_].list_ingress_for_all_namespaces,
            timeout_seconds=5,
            allow_watch_bookmarks=True,
            resource_version=bookmark,
        )


class IP_ADDRESSE_RUNNER(NetworkingV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("NetworkingV1Api_IP_ADDRESSES")

    def fetch_state(self, _):
        bookmark = self.REDIS_CONNECTOR.get_bookmark(_, self.NAME)
        # if bookmark == None : return []
        return self.WATCHERS[_].stream(
            self.CLIENTS[_].list_ip_address,
            timeout_seconds=5,
            allow_watch_bookmarks=True,
            resource_version=bookmark,
        )


class NETWORK_POLICY_RUNNER(NetworkingV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("NetworkingV1Api_NETWORK_POLICIES")

    def fetch_state(self, _):
        bookmark = self.REDIS_CONNECTOR.get_bookmark(_, self.NAME)
        # if bookmark == None : return []
        return self.WATCHERS[_].stream(
            self.CLIENTS[_].list_network_policy_for_all_namespaces,
            timeout_seconds=5,
            allow_watch_bookmarks=True,
            resource_version=bookmark,
        )


class SERVICE_CIRD_RUNNER(NetworkingV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("NetworkingV1Api_SERVICE_CIRDS")

    def fetch_state(self, _):
        bookmark = self.REDIS_CONNECTOR.get_bookmark(_, self.NAME)
        # if bookmark == None : return []
        return self.WATCHERS[_].stream(
            self.CLIENTS[_].list_service_cidr,
            timeout_seconds=5,
            allow_watch_bookmarks=True,
            resource_version=bookmark,
        )
