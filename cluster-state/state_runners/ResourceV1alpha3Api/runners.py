from state_runners.base.base_runner import BASE_RUNNER

from kubernetes import client


class ResourceV1alpha3Api_RUNNER(BASE_RUNNER):
    def __init__(self, name) -> None:
        super().__init__(client.ResourceV1alpha3Api, name)


class DEVICE_CLASS_RUNNER(ResourceV1alpha3Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("ResourceV1alpha3Api_DEVICE_CLASSES")

    def fetch_state(self, _):
        return self.CLIENTS[_].list_device_class(
            **{"timeout_seconds": 20, "_request_timeout": 20}
        )


class DEVICE_TAINT_RULE_RUNNER(ResourceV1alpha3Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("ResourceV1alpha3Api_DEVICE_TAINT_RULES")

    def fetch_state(self, _):
        return self.CLIENTS[_].list_device_taint_rule(
            **{"timeout_seconds": 20, "_request_timeout": 20}
        )


class RESOURCE_CLAIM_RUNNER(ResourceV1alpha3Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("ResourceV1alpha3Api_RESOURCE_CLAIMS")

    def fetch_state(self, _):
        return self.CLIENTS[_].list_resource_claim_for_all_namespaces(
            **{"timeout_seconds": 20, "_request_timeout": 20}
        )


class RESOURCE_CLAIM_TEMPLATE_RUNNER(ResourceV1alpha3Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("ResourceV1alpha3Api_RESOURCE_CLAIM_TEMPLATES")

    def fetch_state(self, _):
        return self.CLIENTS[_].list_resource_claim_template_for_all_namespaces(
            **{"timeout_seconds": 20, "_request_timeout": 20}
        )


class RESOURCE_SLICE_RUNNER(ResourceV1alpha3Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("ResourceV1alpha3Api_RESOURCE_SLICES")

    def fetch_state(self, _):
        return self.CLIENTS[_].list_resource_slice(
            **{"timeout_seconds": 20, "_request_timeout": 20}
        )
