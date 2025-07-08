import redis
import os
from redis.backoff import ExponentialBackoff
from redis.retry import Retry
from redis.exceptions import ConnectionError, TimeoutError


class REDIS_CONNECTOR:
    def __init__(self) -> None:
        self.init_pool()
        self.init_connection()

    def init_pool(self) -> None:
        self.BACKOFF = ExponentialBackoff(base=1, cap=3)
        self.RETRY = Retry(self.BACKOFF, retries=3)

        self.POOL = redis.ConnectionPool(
            host="redis",
            port=6379,
            db=0,
            username=os.getenv("CLUSTER_STATE_REDIS_CRED_USER"),
            password=os.getenv("CLUSTER_STATE_REDIS_CRED_PASSWD"),
            max_connections=250,
            decode_responses=True,
            retry=self.RETRY,
            retry_on_error=[ConnectionError, TimeoutError],
        )

    def init_connection(self) -> None:
        self.CONNECTION = redis.Redis(
            connection_pool=self.POOL, health_check_interval=3
        )

    def create_json_and_path(self, cluster: str, resource_type: str) -> None:
        if not self.CONNECTION.exists(f"CLUSTER_DATA:{cluster}"):
            self.CONNECTION.json().set(f"CLUSTER_DATA:{cluster}", "$", {})
        if self.CONNECTION.json().type(
            f"CLUSTER_DATA:{cluster}", f"$.{resource_type}"
        ) in [None, [None], []]:
            self.CONNECTION.json().set(
                f"CLUSTER_DATA:{cluster}", f"$.{resource_type}", {}
            )

    def update_resource(
        self, cluster: str, resource_type: str, data: dict
    ) -> str | None:
        self.create_json_and_path(cluster, resource_type)

        latest_resource_version = self.CONNECTION.get(
            f"RESOURCE_VERSION_BOOKMARKS:{cluster}|{resource_type}"
        )
        resource_s_version = self.CONNECTION.json().get(
            f"CLUSTER_DATA:{cluster}",
            f"$.{resource_type}.{data["metadata"]["uid"]}.metadata.resource_version",
        )

        if latest_resource_version is not None and int(
            str(latest_resource_version)
        ) <= int(data["metadata"]["resource_version"]):
            self.CONNECTION.json().set(
                f"CLUSTER_DATA:{cluster}",
                f"$.{resource_type}.{data["metadata"]["uid"]}",
                data,
            )
            return

        if (
            not resource_s_version == None
            and not resource_s_version == [None]
            and not resource_s_version == []
            and int(str(resource_s_version[0]))
            <= int(data["metadata"]["resource_version"])
        ):
            self.CONNECTION.json().set(
                f"CLUSTER_DATA:{cluster}",
                f"$.{resource_type}.{data["metadata"]["uid"]}",
                data,
            )
            return

        if latest_resource_version == None and resource_s_version in [None, [None], []]:
            self.CONNECTION.json().set(
                f"CLUSTER_DATA:{cluster}",
                f"$.{resource_type}.{data["metadata"]["uid"]}",
                data,
            )
