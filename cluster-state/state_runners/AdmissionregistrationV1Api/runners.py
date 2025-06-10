from state_runners.base.base_runner import BASE_RUNNER

from kubernetes import client


class AdmissionregistrationV1Api_RUNNER(BASE_RUNNER):
    def __init__(self, name) -> None:
        super().__init__(client.AdmissionregistrationV1Api, name)


class MUTATING_WEBHOOK_CONFIG_RUNNER(AdmissionregistrationV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("AdmissionregistrationV1Api_MUTATING_WEBHOOK_CONFIGS")

    def fetch_state(self, _):
        return self.CLIENTS[_].list_mutating_webhook_configuration(
            **{"timeout_seconds": 20, "_request_timeout": 20}
        )


class VALIDATING_ADMISSION_POLICY_RUNNER(AdmissionregistrationV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("AdmissionregistrationV1Api_VALIDATING_ADMISSION_POLICIES")

    def fetch_state(self, _):
        return self.CLIENTS[_].list_validating_admission_policy(
            **{"timeout_seconds": 20, "_request_timeout": 20}
        )


class VALIDATING_ADMISSION_POLICY_BINDING_RUNNER(AdmissionregistrationV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__(
            "AdmissionregistrationV1Api_VALIDATING_ADMISSION_POLICY_BINDINGS"
        )

    def fetch_state(self, _):
        return self.CLIENTS[_].list_validating_admission_policy_binding(
            **{"timeout_seconds": 20, "_request_timeout": 20}
        )


class VALIDATING_WEBHOOK_CONFIG_RUNNER(AdmissionregistrationV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("AdmissionregistrationV1Api_VALIDATING_WEBHOOK_CONFIGS")

    def fetch_state(self, _):
        return self.CLIENTS[_].list_validating_webhook_configuration(
            **{"timeout_seconds": 20, "_request_timeout": 20}
        )
