from state_runners.base.base_runner import BASE_RUNNER


class BatchV1Api_RUNNER(BASE_RUNNER):
    def __init__(self, name) -> None:
        super().__init__(name)


class JOB_RUNNER(BatchV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("BatchV1Api_JOBS")

    def get_object_data(self, _):
        return {}


class CRON_JOB_RUNNER(BatchV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("BatchV1Api_CRON_JOBS")

    def get_object_data(self, _):
        return {}
