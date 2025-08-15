from state_runners.base.base_runner import BASE_RUNNER


class AdmissionregistrationV1Api_RUNNER(BASE_RUNNER):
    def __init__(self, name) -> None:
        super().__init__(name)


class MUTATING_WEBHOOK_CONFIG_RUNNER(AdmissionregistrationV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("AdmissionregistrationV1Api_MUTATING_WEBHOOK_CONFIGS")

    def get_object_data(self, _):
        return {}


class VALIDATING_ADMISSION_POLICY_RUNNER(AdmissionregistrationV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("AdmissionregistrationV1Api_VALIDATING_ADMISSION_POLICIES")

    def get_object_data(self, _):
        return {}


class VALIDATING_ADMISSION_POLICY_BINDING_RUNNER(AdmissionregistrationV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__(
            "AdmissionregistrationV1Api_VALIDATING_ADMISSION_POLICY_BINDINGS"
        )

    def get_object_data(self, _):
        return {}

class VALIDATING_WEBHOOK_CONFIG_RUNNER(AdmissionregistrationV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("AdmissionregistrationV1Api_VALIDATING_WEBHOOK_CONFIGS")

    def get_object_data(self, _):
        return {}
