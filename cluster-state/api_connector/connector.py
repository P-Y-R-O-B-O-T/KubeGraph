import httpx
import os
import time
from rich.console import Console


class APIConnector:
    def __init__(self) -> None:
        self.TOKEN = None
        self.BASE_URL = "http://nginx:80/api"
        self.USERNAME = os.getenv("CLUSTER_STATE_API_CRED_USER")
        self.PASSWORD = os.getenv("CLUSTER_STATE_API_CRED_PASSWD")
        self.RICH_CONSOLE = Console(
            force_terminal=True,
            color_system="truecolor",
            log_path=False,
            safe_box=False,
        )

    def get_token(self, resource_type: str) -> None:
        while True:
            self.RICH_CONSOLE.log(f"Fetching api TOKEN {resource_type}")
            try:
                self.get_token_once(resource_type)
                break
            except Exception as E:
                self.RICH_CONSOLE.log(f"{E}")
            time.sleep(1)

    def get_token_once(self, resource_type: str) -> None:
        self.RICH_CONSOLE.log(f"Trying to get authenticated {resource_type}")
        response = httpx.post(
            f"{self.BASE_URL}/auth/token",
            data={"username": self.USERNAME, "password": self.PASSWORD},
        )
        response.raise_for_status()
        self.TOKEN = response.json()["access_token"]
        self.RICH_CONSOLE.log(f"Got TOKEN {resource_type}")

    def upload_data(self, cluster_name: str, resource_type: str, data: dict) -> None:
        if self.TOKEN is None:
            self.get_token(resource_type)
        try:
            self.RICH_CONSOLE.log(f"Updating {cluster_name} {resource_type} to api")
            response = httpx.post(
                f"{self.BASE_URL}/cluster/data",
                json={
                    "cluster_name": cluster_name,
                    "resource_type": resource_type,
                    "cluster_data": data,
                },
                headers={"Authorization": f"Bearer {self.TOKEN}"},
            )
            response.raise_for_status()
            self.RICH_CONSOLE.log(f"Updated {cluster_name} {resource_type} to api")
        except Exception as E:
            self.RICH_CONSOLE.log(f"Update failed {cluster_name} {resource_type}")
            self.RICH_CONSOLE.log(f"{E}")
