from state_runners.base.base_runner import BASE_RUNNER
from kubernetes import client


class BatchV1Api_RUNNER(BASE_RUNNER):
    def __init__(self, name) -> None:
        super().__init__(client.BatchV1Api, name)


class JOB_RUNNER(BatchV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("BatchV1Api_JOBS")

    def fetch_state(self, _):
        return self.WATCHERS[_].stream(
            self.CLIENTS[_].list_job_for_all_namespaces,
            timeout_seconds=5,
            allow_watch_bookmarks=True,
            resource_version=self.LATEST_RESOURCE_VERSION,
        )


class CRON_JOB_RUNNER(BatchV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("BatchV1Api_CRON_JOBS")

    def fetch_state(self, _):
        return self.WATCHERS[_].stream(
            self.CLIENTS[_].list_cron_job_for_all_namespaces,
            timeout_seconds=5,
            allow_watch_bookmarks=True,
            resource_version=self.LATEST_RESOURCE_VERSION,
        )
