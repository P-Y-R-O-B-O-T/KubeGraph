from state_runners.base.base_runner import BASE_RUNNER
from kubernetes import client


class FlowcontrolApiserverV1Api_RUNNER(BASE_RUNNER):
    def __init__(self, name) -> None:
        super().__init__(client.FlowcontrolApiserverV1Api, name)


class FLOW_SCHEMA_RUNNER(FlowcontrolApiserverV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("FlowcontrolApiserverV1Api_FLOW_SCHEMAS")

    def get_object_data(self, _):
        return {}


class PRIORITY_LEVEL_CONFIG_RUNNER(FlowcontrolApiserverV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("FlowcontrolApiserverV1Api_PRIORITY_LEVEL_CONFIGS")

    def get_object_data(self, _):
        return {}
