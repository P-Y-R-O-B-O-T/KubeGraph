from state_runners.base.base_runner import BASE_RUNNER
from kubernetes import client


class ApiextensionsV1Api_RUNNER(BASE_RUNNER):
    def __init__(self, name) -> None:
        super().__init__(client.ApiextensionsV1Api, name)


class CUSTOM_RESOURCE_DEFINITION_RUNNER(ApiextensionsV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("ApiextensionsV1Api_MUTATING_WEBHOOK_CONFIGS")

    def fetch_state(self, _):
        return self.WATCHERS[_].stream(
            self.CLIENTS[_].list_custom_resource_definition,
            timeout_seconds=5,
            allow_watch_bookmarks=True,
            resource_version=self.LATEST_RESOURCE_VERSION.get(_),
        )
