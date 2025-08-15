from state_runners.base.base_runner import BASE_RUNNER


class NodeV1Api_RUNNER(BASE_RUNNER):
    def __init__(self, name) -> None:
        super().__init__(name)


class RUNTIME_CLASS_RUNNER(NodeV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("NodeV1Api_RUNTIME_CLASSES")

    def get_object_data(self, _):
        return {}
