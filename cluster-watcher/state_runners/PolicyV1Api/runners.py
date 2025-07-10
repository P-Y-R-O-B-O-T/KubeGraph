from state_runners.base.base_runner import BASE_RUNNER
from kubernetes import client


class PolicyV1Api_RUNNER(BASE_RUNNER):
    def __init__(self, name) -> None:
        super().__init__(client.PolicyV1Api, name)


class POD_DISRUPTION_BUDGET_RUNNER(PolicyV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("PolicyV1Api_POD_DISRUPTION_BUDGETS")

    def fetch_state(self, _):
        bookmark = self.REDIS_CONNECTOR.get_bookmark(_, self.NAME)
        # if bookmark == None : return []
        return self.WATCHERS[_].stream(
            self.CLIENTS[_].list_pod_disruption_budget_for_all_namespaces,
            timeout_seconds=5,
            allow_watch_bookmarks=True,
            resource_version=bookmark,
        )
