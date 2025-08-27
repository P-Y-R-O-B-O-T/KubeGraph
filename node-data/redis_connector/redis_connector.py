import redis
import os
import json
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
            username=os.getenv("NODE_DATA_REDIS_CRED_USER"),
            password=os.getenv("NODE_DATA_REDIS_CRED_PASSWD"),
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

    def update_node_data(self, cleaned_data: dict, current_update: dict) -> bool | None:
        # ...
        # ...
        # ...
        self.CONNECTION.lpop("CLUSTER_DATA:UPDATES_QUEUE")
        pass

    def get_cluster_data(self, cluster: str) -> dict | None:
        pass

    def get_update_notification(self) -> dict | None:
        update_items = self.CONNECTION.lrange("CLUSTER_DATA:UPDATES_QUEUE", 0, 0)

        if update_items == []:
            return
        return json.loads(update_items[0])

    def get_updated_resource_data(self, update_notification: dict) -> dict | None:
        pass
