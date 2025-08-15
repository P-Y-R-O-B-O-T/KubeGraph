from state_runners.base.base_runner import BASE_RUNNER


class AutoscalingV2Api_RUNNER(BASE_RUNNER):
    def __init__(self, name) -> None:
        super().__init__(name)


class HPA_RUNNER(AutoscalingV2Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("AutoscalingV2Api_HPAS")

    def get_object_data(self, _):
        return {}
