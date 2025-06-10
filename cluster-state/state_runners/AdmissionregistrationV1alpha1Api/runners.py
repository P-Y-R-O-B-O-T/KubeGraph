from state_runners.base.base_runner import BASE_RUNNER

from kubernetes import client


class AdmissionregistrationV1alpha1Api_RUNNER(BASE_RUNNER):
    def __init__(self, name) -> None:
        super().__init__(client.AdmissionregistrationV1alpha1Api, name)


class MUTATING_ADMISSION_POLICY_RUNNER(AdmissionregistrationV1alpha1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("AdmissionregistrationV1alpha1Api_MUTATING_ADMISSION_POLICIES")

    def fetch_state(self, _):
        return self.CLIENTS[_].list_mutating_admission_policy(
            **{"timeout_seconds": 20, "_request_timeout": 20}
        )

class MUTATING_ADMISSION_POLICY_BINDING_RUNNER(AdmissionregistrationV1alpha1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("AdmissionregistrationV1alpha1Api_MUTATING_ADMISSION_POLICY_BINDINGS")

    def fetch_state(self, _):
        return self.CLIENTS[_].list_mutating_admission_policy_binding(
            **{"timeout_seconds": 20, "_request_timeout": 20}
        )
