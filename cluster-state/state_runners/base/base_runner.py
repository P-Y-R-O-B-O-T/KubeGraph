from abc import abstractmethod
from typing import Any
from rich.console import Console
import asyncio
import os
import sys
import time
from datetime import datetime
import traceback

import constants.constants as CONSTANTS
import kubeconfig_utils.utils as KUBECONFIG_UTILS
from api_connector.connector import APIConnector


class BASE_RUNNER:
    def __init__(self, api_object_class, name: str) -> None:
        self.RICH_CONSOLE = Console(
            force_terminal=True,
            color_system="truecolor",
            log_path=False,
            safe_box=False,
        )
        self.STACK_API_CONNECTOR = APIConnector()
        self.API_OBJECT_CLASS = api_object_class
        self.NAME = name

    def convert_datetimes_to_strings(self, obj: Any) -> Any:
        if isinstance(obj, dict):
            return {
                key: self.convert_datetimes_to_strings(value)
                for key, value in obj.items()
            }
        elif isinstance(obj, (list, tuple)):
            return [self.convert_datetimes_to_strings(item) for item in obj]
        elif isinstance(obj, datetime):
            return obj.isoformat()
        else:
            return obj

    def load_clients(self) -> None:
        self.RICH_CONSOLE.print(f"Loading files {self.NAME}")
        self.API_CLIENTS = {}
        self.FILES = os.listdir(CONSTANTS.KUBECONF_PATH)

        to_be_removed = []

        for _ in self.FILES:
            try:
                self.API_CLIENTS[_] = KUBECONFIG_UTILS.get_api_client(
                    os.path.join(CONSTANTS.KUBECONF_PATH, _)
                )
            except:
                to_be_removed.append(_)

        self.CLIENTS = {}
        for _ in self.API_CLIENTS:
            try:
                self.CLIENTS[_] = self.API_OBJECT_CLASS(api_client=self.API_CLIENTS[_])
            except:
                if _ not in to_be_removed:
                    to_be_removed.append(_)

        for _ in to_be_removed:
            self.FILES.remove(_)
        self.RICH_CONSOLE.print(f"Loaded files {self.NAME}")

    async def run(self) -> None:
        while True:
            self.load_clients()
            await asyncio.sleep(2)

            while True:

                for _ in self.CLIENTS:

                    start_time = time.time()
                    try:
                        self.RICH_CONSOLE.log(
                            f"[khaki1]Fetching[/ khaki1] [slate_blue1]{_[:_.find(".")]}[/ slate_blue1] | [light_salmon1]{self.NAME}[/ light_salmon1]"
                        )
                        fetched = self.fetch_state(
                            _
                        )  # await asyncio.to_thread(self.fetch_state, _)
                        self.RICH_CONSOLE.log(
                            f"[spring_green1]Fetched[/ spring_green1]  [slate_blue1]{_[:_.find(".")]}[/ slate_blue1] | [light_salmon1]{self.NAME}[/ light_salmon1] in {time.time() - start_time}"
                        )

                        structured_data = self.structure_data(fetched.to_dict())
                        self.STACK_API_CONNECTOR.upload_data(
                            _, self.NAME, structured_data
                        )

                    except:
                        self.RICH_CONSOLE.log(
                            f"[deep_pink3]Error[/ deep_pink3] fetching [slate_blue1]{_[:_.find(".")]}[/ slate_blue1] | [light_salmon1]{self.NAME}[/ light_salmon1]"
                        )
                        self.RICH_CONSOLE.log(traceback.format_exc())

                if self.need_file_reload():
                    break
                await asyncio.sleep(10)

    def structure_data(self, fetched: dict) -> dict:
        data = {}
        for _ in fetched["items"]:
            data[_["metadata"]["name"]] = _
        return self.convert_datetimes_to_strings(data)

    def need_file_reload(self) -> bool:
        return sorted(self.FILES) != sorted(os.listdir(CONSTANTS.KUBECONF_PATH))

    def logtime(self) -> str:
        return datetime.now().strftime("[ %Y-%m-%d %H:%M:%S ]")

    @abstractmethod
    def fetch_state(self, _):
        raise NotImplementedError("Subclasses must implement fetch_state")
