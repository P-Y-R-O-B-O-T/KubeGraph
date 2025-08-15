from state_runners.base.base_runner import BASE_RUNNER


class AppsV1Api_RUNNER(BASE_RUNNER):
    def __init__(self, name) -> None:
        super().__init__(name)


class CONTROLLER_VERSION_RUNNER(AppsV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("AppsV1Api_CONTROLLER_VERSIONS")

    def get_object_data(self, _):
        return {}


class DAEMONSET_RUNNER(AppsV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("AppsV1Api_DAEMONSETS")

    def get_object_data(self, _):
        return {}


class DEPLOYMENT_RUNNER(AppsV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("AppsV1Api_DEPLOYMENTS")

    def get_object_data(self, _):
        return {}


class REPLICASET_RUNNER(AppsV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("AppsV1Api_REPLICASETS")

    def get_object_data(self, _):
        return {}


class STATEFULSET_RUNNER(AppsV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("AppsV1Api_STATEFULSETS")

    def get_object_data(self, _):
        return {}
