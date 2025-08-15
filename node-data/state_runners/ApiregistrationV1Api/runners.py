from state_runners.base.base_runner import BASE_RUNNER


class ApiregistrationV1Api_RUNNER(BASE_RUNNER):
    def __init__(self, name) -> None:
        super().__init__(name)


class API_SERVICE_RUNNER(ApiregistrationV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("ApiregistrationV1Api_API_SERVICES")

    def get_object_data(self, _):
        return {}
