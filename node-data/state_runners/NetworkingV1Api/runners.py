from state_runners.base.base_runner import BASE_RUNNER


class NetworkingV1Api_RUNNER(BASE_RUNNER):
    def __init__(self, name) -> None:
        super().__init__(name)


class INGRESS_CLASS_RUNNER(NetworkingV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("NetworkingV1Api_INGRESS_CLASSES")

    def get_object_data(self, _):
        return {}


class INGRESS_RUNNER(NetworkingV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("NetworkingV1Api_INGRESSES")

    def get_object_data(self, _):
        return {}


class IP_ADDRESSE_RUNNER(NetworkingV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("NetworkingV1Api_IP_ADDRESSES")

    def get_object_data(self, _):
        return {}


class NETWORK_POLICY_RUNNER(NetworkingV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("NetworkingV1Api_NETWORK_POLICIES")

    def get_object_data(self, _):
        return {}


class SERVICE_CIRD_RUNNER(NetworkingV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("NetworkingV1Api_SERVICE_CIRDS")

    def get_object_data(self, _):
        return {}
