from state_runners.base.base_runner import BASE_RUNNER
from kubernetes import client


class CertificatesV1Api_RUNNER(BASE_RUNNER):
    def __init__(self, name) -> None:
        super().__init__(client.CertificatesV1Api, name)


class CSR_RUNNER(CertificatesV1Api_RUNNER):
    def __init__(self) -> None:
        super().__init__("CertificatesV1Api_CSRS")

    def fetch_state(self, _):
        bookmark = self.REDIS_CONNECTOR.get_bookmark(_, self.NAME)
        # if bookmark == None : return []
        return self.WATCHERS[_].stream(
            self.CLIENTS[_].list_certificate_signing_request,
            timeout_seconds=5,
            allow_watch_bookmarks=True,
            resource_version=bookmark,
        )
