from state_runners.base.base_runner import BASE_RUNNER
from kubernetes import client


class ApiregistrationV1Api_RUNNER(BASE_RUNNER):
    def __init__(self, name) -> None:
        super().__init__(client.ApiregistrationV1Api, name)


class API_SERVICE_RUNNER(ApiregistrationV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("ApiregistrationV1Api_API_SERVICES")

    def fetch_state(self, _):
        return self.WATCHERS[_].stream(
            self.CLIENTS[_].list_api_service,
            timeout_seconds=5,
            allow_watch_bookmarks=True,
            resource_version=self.LATEST_RESOURCE_VERSION,
        )
