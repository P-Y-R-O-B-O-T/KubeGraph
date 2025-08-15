from state_runners.base.base_runner import BASE_RUNNER


class ApiextensionsV1Api_RUNNER(BASE_RUNNER):
    def __init__(self, name) -> None:
        super().__init__(name)


class CUSTOM_RESOURCE_DEFINITION_RUNNER(ApiextensionsV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("ApiextensionsV1Api_CUSTOM_RESOURCE_DEFINITIONS")

    def get_object_data(self, _):
        return {}
