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
            self.RICH_CONSOLE.log(f"[khaki1]Fetching[/ khaki1] AUTH TOKEN [light_salmon1]{resource_type}[/ light_salmon1]")
            try:
                self.get_token_once(resource_type)
                break
            except Exception as E:
                self.RICH_CONSOLE.log(f"[deep_pink3]Error[/ deep_pink3] getting AUTH TOKEN [light_salmon1]{resource_type}[/ light_salmon1]")
                self.RICH_CONSOLE.log(f"{E}")
            time.sleep(1)

    def get_token_once(self, resource_type: str) -> None:
        self.RICH_CONSOLE.log(f"[khaki1]Trying[/ khaki1] to get AUTH TOKEN [light_salmon1]{resource_type}[/ light_salmon1]")
        response = httpx.post(
            f"{self.BASE_URL}/auth/token",
            data={"username": self.USERNAME, "password": self.PASSWORD},
        )
        response.raise_for_status()
        self.TOKEN = response.json()["access_token"]
        self.RICH_CONSOLE.log(f"[spring_green1]Fetched[/ spring_green1] AUTH TOKEN [light_salmon1]{resource_type}[/ light_salmon1]")

    def upload_data(self, cluster_name: str, resource_type: str, data: dict) -> None:
        if self.TOKEN is None:
            self.get_token(resource_type)
        try:
            self.RICH_CONSOLE.log(f"[khaki1]Updating[/ khaki1] [slate_blue1]{cluster_name}[/ slate_blue1] | [light_salmon1]{resource_type}[/ light_salmon1] to STACK API")
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
            self.RICH_CONSOLE.log(f"[spring_green1]Updated[/ spring_green1] [slate_blue1]{cluster_name}[/ slate_blue1] | [light_salmon1]{resource_type}[/ light_salmon1] to STACK API")
        except Exception as E:
            self.RICH_CONSOLE.log(f"[deep_pink3]Error[/ deep_pink3] updating [slate_blue1]{cluster_name}[/ slate_blue1] | [light_salmon1]{resource_type}[/ light_salmon1] to STACK API")
            self.RICH_CONSOLE.log(f"{E}")
