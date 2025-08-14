from state_runners.base.base_runner import BASE_RUNNER
from kubernetes import client


class PolicyV1Api_RUNNER(BASE_RUNNER):
    def __init__(self, name) -> None:
        super().__init__(client.PolicyV1Api, name)


class POD_DISRUPTION_BUDGET_RUNNER(PolicyV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("PolicyV1Api_POD_DISRUPTION_BUDGETS")

    def get_object_data(self, _):
        return {}
