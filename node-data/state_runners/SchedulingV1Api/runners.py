from state_runners.base.base_runner import BASE_RUNNER


class SchedulingV1Api_RUNNER(BASE_RUNNER):
    def __init__(self, name) -> None:
        super().__init__(name)


class PRIORITY_CLASS_RUNNER(SchedulingV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("SchedulingV1Api_PRIORITY_CLASSES")

    def get_object_data(self, _):
        return {}
