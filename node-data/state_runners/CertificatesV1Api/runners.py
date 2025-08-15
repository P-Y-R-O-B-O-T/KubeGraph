from state_runners.base.base_runner import BASE_RUNNER


class CertificatesV1Api_RUNNER(BASE_RUNNER):
    def __init__(self, name) -> None:
        super().__init__(name)


class CSR_RUNNER(CertificatesV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("CertificatesV1Api_CSRS")

    def get_object_data(self, _):
        return {}
