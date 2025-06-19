
from state_runners.base.base_runner import BASE_RUNNER
from kubernetes import client, watch
from kubernetes.client.exceptions import ApiException


class NetworkingV1Api_RUNNER(BASE_RUNNER):
    def __init__(self, name) -> None:
        super().__init__(client.NetworkingV1Api, name)


class INGRESS_CLASS_RUNNER(NetworkingV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("NetworkingV1Api_INGRESS_CLASSES")

    def fetch_state(self, _):
        w = watch.Watch()
        try:
            return w.stream(self.CLIENTS[_].list_ingress_class, timeout_seconds=0)
        except ApiException as e:
            # ❌ Watch may not be supported for IngressClass
            print(f"[WARNING] Watch not supported for INGRESS_CLASSES: {e}")
            return self.CLIENTS[_].list_ingress_class()


class INGRESS_RUNNER(NetworkingV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("NetworkingV1Api_INGRESSES")

    def fetch_state(self, _):
        w = watch.Watch()
        return w.stream(self.CLIENTS[_].list_ingress_for_all_namespaces, timeout_seconds=0)


class IP_ADDRESSE_RUNNER(NetworkingV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("NetworkingV1Api_IP_ADDRESSES")

    def fetch_state(self, _):
        w = watch.Watch()
        try:
            return w.stream(self.CLIENTS[_].list_ip_address, timeout_seconds=0)
        except ApiException as e:
            # ❌ Watch likely not supported for IPAddress (alpha feature)
            print(f"[WARNING] Watch not supported for IP_ADDRESSES: {e}")
            return self.CLIENTS[_].list_ip_address()


class NETWORK_POLICY_RUNNER(NetworkingV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("NetworkingV1Api_NETWORK_POLICIES")

    def fetch_state(self, _):
        w = watch.Watch()
        return w.stream(self.CLIENTS[_].list_network_policy_for_all_namespaces, timeout_seconds=0)


class SERVICE_CIRD_RUNNER(NetworkingV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("NetworkingV1Api_SERVICE_CIRDS")

    def fetch_state(self, _):
        w = watch.Watch()
        try:
            return w.stream(self.CLIENTS[_].list_service_cidr, timeout_seconds=0)
        except ApiException as e:
            # ❌ Watch likely not supported for ServiceCIDR (alpha feature)
            print(f"[WARNING] Watch not supported for SERVICE_CIRDS: {e}")
            return self.CLIENTS[_].list_service_cidr()
