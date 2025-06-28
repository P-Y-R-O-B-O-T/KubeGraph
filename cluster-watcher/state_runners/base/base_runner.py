from abc import abstractmethod
from rich.console import Console
import asyncio
import os
import sys
import time
from datetime import datetime
import traceback

import constants.constants as CONSTANTS
import kubeconfig_utils.utils as KUBECONFIG_UTILS
from MonitoringMessage.Message import MonitoringMessage
from  api_connector.connector import APIConnector

class BASE_RUNNER:
    def __init__(self, api_object_class, name: str) -> None:
        self.RICH_CONSOLE = Console(
            force_terminal=True,
            color_system="truecolor",
            log_path=False,
            safe_box=False,
        )

        self.API_OBJECT_CLASS = api_object_class
        self.STACK_API_CONNECTOR = APIConnector()
        self.NAME = name

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

    async def watch_cluster(self, cluster_name: str, fetch_state):
        while True:
            try:
                self.RICH_CONSOLE.log(
                    f"[khaki1]Starting watch[/ khaki1] for [slate_blue1]{cluster_name}[/ slate_blue1] | [light_salmon1]{self.NAME}[/ light_salmon1]"
                )

                events = await asyncio.to_thread(fetch_state, cluster_name)

                for event in events:
                    
                    obj = event["object"].to_dict()
                    event_type = event["type"]
                    metadata = obj.get("metadata", {})
                    name = metadata.get("name")
                    namespace = metadata.get("namespace", "default")

                    msg = MonitoringMessage(
                    cluster_name=cluster_name,
                    resource_name=name,
                    namespace=namespace,
                    action=event_type,
                    timestamp=datetime.utcnow(),
                    data=obj,

                )
                    
                    self.STACK_API_CONNECTOR.push_updates(cluster_name=cluster_name, resource_type=self.NAME, data=msg)
                 
                    self.RICH_CONSOLE.print(f"[{cluster_name}] {event_type}: [bold green]{name}[/bold green]")


            except Exception as e:
                self.RICH_CONSOLE.log(
                    f"[deep_pink3]Error[/ deep_pink3] watching [slate_blue1]{cluster_name}[/ slate_blue1]: {e}"
                )
                self.RICH_CONSOLE.log(traceback.format_exc())
                await asyncio.sleep(2)

    async def run(self) -> None:
        while True:
            self.load_clients()
            await asyncio.sleep(2)

            while True:
                tasks = []  

                for _ in self.CLIENTS:
                    DATA = {}

                    self.RICH_CONSOLE.log(
                        f"[khaki1]Fetching[/ khaki1] [slate_blue1]{_[:_.find('.')]}[/ slate_blue1] | [light_salmon1]{self.NAME}[/ light_salmon1]"
                    )
                    start_time = time.time()

                    try:
                        ## create a task that can be run in parallel.
                        task = asyncio.create_task(self.watch_cluster(_, self.fetch_state))
                        tasks.append(task)

                        await asyncio.gather(*tasks)
                        self.RICH_CONSOLE.log(
                            f"[spring_green1]Fetched[/ spring_green1]  [slate_blue1]{_[:_.find('.')]}[/ slate_blue1] | [light_salmon1]{self.NAME}[/ light_salmon1] in {time.time() - start_time}"
                        )
                    except:
                        self.RICH_CONSOLE.log(
                            f"[deep_pink3]Error[/ deep_pink3] fetching [slate_blue1]{_[:_.find('.')]}[/ slate_blue1] | [light_salmon1]{self.NAME}[/ light_salmon1]"
                        )
                        self.RICH_CONSOLE.log(traceback.format_exc())

                if self.need_file_reload():
                    break
                await asyncio.sleep(10)

    def structure_data(self, DATA, fetched: dict) -> None:
        for _ in fetched["items"]:
            DATA[_["metadata"]["name"]] = _

    def need_file_reload(self) -> bool:
        return sorted(self.FILES) != sorted(os.listdir(CONSTANTS.KUBECONF_PATH))

    def logtime(self) -> str:
        return datetime.now().strftime("[ %Y-%m-%d %H:%M:%S ]")

    @abstractmethod
    def fetch_state(self, _):
        raise NotImplementedError("Subclasses must implement fetch_state")

