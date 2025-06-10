
from state_runners.base.base_runner import BASE_RUNNER

from kubernetes import client


class EventsV1Api_RUNNER(BASE_RUNNER):
    def __init__(self, name) -> None:
        super().__init__(client.EventsV1Api, name)


class EVENTS_RUNNER(EventsV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("EventsV1Api_EVENTS")

    def fetch_state(self, _):
        return self.CLIENTS[_].list_event_for_all_namespaces(
            **{"timeout_seconds": 20, "_request_timeout": 20}
        )
