
from state_runners.base.base_runner import BASE_RUNNER

from kubernetes import client


class LogsApi_RUNNER(BASE_RUNNER):
    def __init__(self, name) -> None:
        super().__init__(client.LogsApi, name)


class LOG_FILE_LIST_HANDLER_RUNNER(LogsApi_RUNNER):
    def __init__(self) -> None:
        super().__init__("LogsApi_LOG_FILE_LIST_HANDLERS")

    def fetch_state(self, _):
        return self.CLIENTS[_].log_file_list_handler(
            **{"timeout_seconds": 20, "_request_timeout": 20}
        )
