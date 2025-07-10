from state_runners.base.base_runner import BASE_RUNNER
from kubernetes import client


class SchedulingV1Api_RUNNER(BASE_RUNNER):
    def __init__(self, name) -> None:
        super().__init__(client.SchedulingV1Api, name)


class PRIORITY_CLASS_RUNNER(SchedulingV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("SchedulingV1Api_PRIORITY_CLASSES")

    def fetch_state(self, _):
        bookmark = self.REDIS_CONNECTOR.get_bookmark(_, self.NAME)
        # if bookmark == None : return []
        return self.WATCHERS[_].stream(
            self.CLIENTS[_].list_priority_class,
            timeout_seconds=5,
            allow_watch_bookmarks=True,
            resource_version=bookmark,
        )
