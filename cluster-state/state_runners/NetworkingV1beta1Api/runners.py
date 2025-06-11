from state_runners.base.base_runner import BASE_RUNNER

from kubernetes import client


class NetworkingV1beta1Api_RUNNER(BASE_RUNNER):
    def __init__(self, name) -> None:
        super().__init__(client.NetworkingV1beta1Api, name)


class IP_ADDRESS_RUNNER(NetworkingV1beta1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("NetworkingV1beta1Api_IP_ADDRESSES")

    def fetch_state(self, _):
        return self.CLIENTS[_].list_ip_address(
            **{"timeout_seconds": 20, "_request_timeout": 20}
        )


class SERVICE_CIDR_RUNNER(NetworkingV1beta1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("NetworkingV1beta1Api_SERVICE_CIDRS")

    def fetch_state(self, _):
        return self.CLIENTS[_].list_service_cidr(
            **{"timeout_seconds": 20, "_request_timeout": 20}
        )
