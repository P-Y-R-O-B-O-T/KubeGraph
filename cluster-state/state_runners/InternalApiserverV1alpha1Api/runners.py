from state_runners.base.base_runner import BASE_RUNNER

from kubernetes import client


class InternalApiserverV1alpha1Api_RUNNER(BASE_RUNNER):
    def __init__(self, name) -> None:
        super().__init__(client.InternalApiserverV1alpha1Api, name)


class STORAGE_VERSION_RUNNER(InternalApiserverV1alpha1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("InternalApiserverV1alpha1Api_STORAGE_VERSIONS")

    def fetch_state(self, _):
        return self.CLIENTS[_].list_storage_version(
            **{"timeout_seconds": 20, "_request_timeout": 20}
        )
