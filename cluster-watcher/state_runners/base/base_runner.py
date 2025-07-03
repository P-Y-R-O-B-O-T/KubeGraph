from abc import abstractmethod
from rich.console import Console
from typing import Any
import os
import threading
import time
from datetime import datetime
import traceback

from kubernetes import watch

import constants.constants as CONSTANTS
import kubeconfig_utils.utils as KUBECONFIG_UTILS
from api_connector.connector import APIConnector
from kubernetes.client.exceptions import ApiException, ApiTypeError, ApiValueError


class BASE_RUNNER:
    def __init__(self, api_object_class, name: str) -> None:
        self.RICH_CONSOLE = Console(
            force_terminal=True,
            color_system="truecolor",
            log_path=False,
            safe_box=False,
        )

        self.LATEST_RESOURCE_VERSION = {}
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

    def run(self) -> None:
        while True:
            self.load_clients()
            self.create_watchers()

            while True:
                start_time = time.time()

                try:
                    self.RICH_CONSOLE.log(
                        f"[khaki1]Watching[/ khaki1] [light_salmon1]{self.NAME}[/ light_salmon1]"
                    )
                    self.watch_clusters()

                    self.RICH_CONSOLE.log(
                        f"[spring_green1]Watched[/ spring_green1] [light_salmon1]{self.NAME}[/ light_salmon1] in {time.time() - start_time}"
                    )
                except:
                    self.RICH_CONSOLE.log(
                        f"[deep_pink3]Error[/ deep_pink3] watching [light_salmon1]{self.NAME}[/ light_salmon1]"
                    )
                    self.RICH_CONSOLE.log(traceback.format_exc())

                if self.need_file_reload():
                    break
                time.sleep(1)

    def watch_clusters(self):
        threads = {}
        for _ in self.CLIENTS:
            threads[_] = threading.Thread(target=self.watch_cluster, args=(_,))
            threads[_].start()
        for _ in threads:
            threads[_].join()

    def watch_cluster(self, _: str) -> None:
        try:
            self.RICH_CONSOLE.log(
                f"[khaki1]Watching[/ khaki1] [slate_blue1]{_}[/ slate_blue1] | [light_salmon1]{self.NAME}[/ light_salmon1]"
            )
            events = self.fetch_state(_)
            for event in events:
                event_type = event["type"]

                if event_type == "BOOKMARK":
                    self.RICH_CONSOLE.log(
                        f"[gold1]BOOKMARK[/ gold1] for [slate_blue1]{_}[/ slate_blue1] | [light_salmon1]{self.NAME}[/ light_salmon1]"
                    )
                    self.LATEST_RESOURCE_VERSION[_] = event["object"]["metadata"][
                        "resourceVersion"
                    ]
                    continue

                obj = event["object"].to_dict()
                data = self.convert_datetimes_to_strings(obj)

                # self.STACK_API_CONNECTOR.push_updates(
                #     cluster_name=_,
                #     resource_type=self.NAME,
                #     data=data,
                #     event_type=event_type,
                # )

                self.RICH_CONSOLE.log(
                    f"[yellow2]Watch {event_type}[/ yellow2]: [slate_blue1]{_}[/ slate_blue1] | [light_salmon1]{self.NAME}[/ light_salmon1] {obj["metadata"]["name"]} {self.NAME} "
                )
            self.RICH_CONSOLE.log(
                f"[spring_green1]Watched[/ spring_green1] [slate_blue1]{_}[/ slate_blue1] | [light_salmon1]{self.NAME}[/ light_salmon1]"
            )

        except ApiException as e:
            if e.status == 410:
                self.RICH_CONSOLE.log("[red] Resouce version is old [/red]")
                pod_list = self.CLIENTS[_].list_pod_for_all_namespaces()
                self.LATEST_RESOURCE_VERSION = pod_list.metadata.resource_version
            else:
                self.RICH_CONSOLE.log(
                    f"[deep_pink3]Kubernetes API error[/deep_pink3] for [slate_blue1]{_}[/slate_blue1]: {e}"
                )
                self.RICH_CONSOLE.log(traceback.format_exc())
                time.sleep(1)

        except (ApiTypeError, ApiValueError) as e:
            self.RICH_CONSOLE.log(
                f"[yellow]API Client misuse[/yellow] for [slate_blue1]{_}[/slate_blue1]: {e}"
            )
            self.RICH_CONSOLE.log(traceback.format_exc())
            time.sleep(1)

        except Exception as e:
            self.RICH_CONSOLE.log(
                f"[deep_pink3]Error[/ deep_pink3] watching [slate_blue1]{_}[/ slate_blue1]: {e}"
            )
            self.RICH_CONSOLE.log(traceback.format_exc())

    def create_watcher(self, cluster: str) -> None:
        self.WATCHERS[cluster] = watch.Watch()

    def create_watchers(self) -> None:
        self.WATCHERS = {}
        for _ in self.CLIENTS:
            self.create_watcher(_)

    def structure_data(self, DATA, fetched: dict) -> None:
        for _ in fetched["items"]:
            DATA[_["metadata"]["name"]] = _

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

    def need_file_reload(self) -> bool:
        return sorted(self.FILES) != sorted(os.listdir(CONSTANTS.KUBECONF_PATH))

    def logtime(self) -> str:
        return datetime.now().strftime("[ %Y-%m-%d %H:%M:%S ]")

    @abstractmethod
    def fetch_state(self, _):
        raise NotImplementedError("Subclasses must implement fetch_state")
