import redis
import os
from redis.backoff import ExponentialBackoff
from redis.retry import Retry
from redis.exceptions import ConnectionError, TimeoutError


class REDIS_CONNECTOR:
    def __init__(self) -> None:
        self.init_pool()

    def init_pool(self) -> None:
        self.BACKOFF = ExponentialBackoff(base=1, cap=3)
        self.RETRY = Retry(self.BACKOFF, retries=3)

        self.POOL = redis.ConnectionPool(
            host="your_redis_host",
            port=6379,
            db=0,
            username=os.getenv("CLUSTER_WATCH_REDIS_CRED_USER"),
            password=os.getenv("CLUSTER_WATCH_REDIS_CRED_PASSWD"),
            max_connections=5,
            decode_responses=True,
            retry=self.RETRY,
            retry_on_error=[ConnectionError, TimeoutError],
        )

    def init_connection(self) -> None:
        self.CONNECTION = redis.Redis(health_check_interval=3)
