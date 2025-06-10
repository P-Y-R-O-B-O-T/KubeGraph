from state_runners.base.base_runner import BASE_RUNNER

from kubernetes import client


class AdmissionregistrationV1beta1Api_RUNNER(BASE_RUNNER):
    def __init__(self, name) -> None:
        super().__init__(client.AdmissionregistrationV1beta1Api, name)


class VALIDATING_ADMISSION_POLICY_RUNNER(AdmissionregistrationV1beta1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("AdmissionregistrationV1beta1Api_VALIDATING_ADMISSION_POLICIES")

    def fetch_state(self, _):
        return self.CLIENTS[_].list_validating_admission_policy(
            **{"timeout_seconds": 20, "_request_timeout": 20}
        )

class VALIDATING_ADMISSION_POLICY_BINDING_RUNNER(AdmissionregistrationV1beta1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("AdmissionregistrationV1beta1Api_VALIDATING_ADMISSION_POLICY_BINDINGS")

    def fetch_state(self, _):
        return self.CLIENTS[_].list_validating_admission_policy_binding(
            **{"timeout_seconds": 20, "_request_timeout": 20}
        )
