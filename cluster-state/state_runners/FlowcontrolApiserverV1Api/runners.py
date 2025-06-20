from state_runners.base.base_runner import BASE_RUNNER

from kubernetes import client


class FlowcontrolApiserverV1Api_RUNNER(BASE_RUNNER):
    def __init__(self, name) -> None:
        super().__init__(client.FlowcontrolApiserverV1Api, name)


class FLOW_SCHEMA_RUNNER(FlowcontrolApiserverV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("FlowcontrolApiserverV1Api_FLOW_SCHEMAS")

    def fetch_state(self, _):
        return self.CLIENTS[_].list_flow_schema(
            **{"timeout_seconds": 20, "_request_timeout": 20}
        )


class PRIORITY_LEVEL_CONFIG_RUNNER(FlowcontrolApiserverV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("FlowcontrolApiserverV1Api_PRIORITY_LEVEL_CONFIGS")

    def fetch_state(self, _):
        return self.CLIENTS[_].list_priority_level_configuration(
            **{"timeout_seconds": 20, "_request_timeout": 20}
        )
