from state_runners.base.base_runner import BASE_RUNNER


class EventsV1Api_RUNNER(BASE_RUNNER):
    def __init__(self, name) -> None:
        super().__init__(name)


class EVENTS_RUNNER(EventsV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("EventsV1Api_EVENTS")

    def get_object_data(self, _):
        return []
        # MIGHT NOT BE REQUIRED IN FUTURE
