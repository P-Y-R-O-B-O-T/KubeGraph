from state_runners.base.base_runner import BASE_RUNNER
from kubernetes import client


class LogsApi_RUNNER(BASE_RUNNER):
    def __init__(self, name) -> None:
        super().__init__(client.LogsApi, name)


class LOG_FILE_LIST_HANDLER_RUNNER(LogsApi_RUNNER):
    def __init__(self) -> None:
        super().__init__("LogsApi_LOG_FILE_LIST_HANDLERS")

    def fetch_state(self, _):
        bookmark = self.REDIS_CONNECTOR.get_bookmark(_, self.NAME)
        # if bookmark == None : return []
        return self.WATCHERS[_].stream(
            self.CLIENTS[_].log_file_list_handler,
            timeout_seconds=5,
            allow_watch_bookmarks=True,
            resource_version=bookmark,
        )
