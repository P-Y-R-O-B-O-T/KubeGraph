
from state_runners.base.base_runner import BASE_RUNNER

from kubernetes import client


class DiscoveryV1Api_RUNNER(BASE_RUNNER):
    def __init__(self, name) -> None:
        super().__init__(client.DiscoveryV1Api, name)


class ENDPOINT_SLICE_RUNNER(DiscoveryV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("DiscoveryV1Api_ENDPOINT_SLICES")

    def fetch_state(self, _):
        return self.CLIENTS[_].list_endpoint_slice_for_all_namespaces(
            **{"timeout_seconds": 20, "_request_timeout": 20}
        )
