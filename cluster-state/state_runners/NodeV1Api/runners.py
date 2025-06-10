
from state_runners.base.base_runner import BASE_RUNNER

from kubernetes import client


class NodeV1Api_RUNNER(BASE_RUNNER):
    def __init__(self, name) -> None:
        super().__init__(client.NodeV1Api, name)


class RUNTIME_CLASS_RUNNER(NodeV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("NodeV1Api_RUNTIME_CLASSES")

    def fetch_state(self, _):
        return self.CLIENTS[_].list_runtime_class(
            **{"timeout_seconds": 20, "_request_timeout": 20}
        )
