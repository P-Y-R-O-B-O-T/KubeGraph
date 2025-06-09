import asyncio
from typing import Dict, List
from kubernetes import client


from app.dispatcher.event_dispatcher import EventDispatcher
from app.watcher.cluster_watcher import ClusterWatcher
from app.watcher.cluster_watcher import ResourceWatcher



from kubeconfig_utils.utils import load_kubeconfig_client, list_kubeconfig_files
from constants.config import KUBECONF_PATH, WATCH_RESOURCES


class WatcherManager:
    """
    Manages watchers for multiple clusters and resources.
    """

    def __init__(self):
        self.clusters_watchers: Dict[str, ClusterWatcher] = {}
        self.dispatcher = EventDispatcher()
        self.running = False

    async def start(self):
        self.running = True
        while self.running:
            cluster_files = list_kubeconfig_files(KUBECONF_PATH)

            for kubeconfig_path in cluster_files:
                cluster_name = kubeconfig_path.split("/")[-1]  # or parse better
                if cluster_name not in self.clusters_watchers:
                    api_client = load_kubeconfig_client(kubeconfig_path)
                    if api_client is None:
                        print(f"[ERROR] Failed to load client for {cluster_name}, skipping")
                        continue

                    cluster_watcher = ClusterWatcher(cluster_name, api_client, WATCH_RESOURCES, self.dispatcher)
                    await cluster_watcher.start()
                    self.clusters_watchers[cluster_name] = cluster_watcher
                    print(f"[INFO] Started watcher for cluster {cluster_name}")

            # Simple check for removed clusters (optional)
            current_clusters = {f.split("/")[-1] for f in cluster_files}
            to_remove = [c for c in self.clusters_watchers if c not in current_clusters]
            for c in to_remove:
                print(f"[INFO] Stopping watcher for removed cluster {c}")
                await self.clusters_watchers[c].stop()
                del self.clusters_watchers[c]

            await asyncio.sleep(60)  

    async def stop(self):
        self.running = False
        for cluster_watcher in self.clusters_watchers.values():
            await cluster_watcher.stop()

    def get_dispatcher(self) -> EventDispatcher:
        return self.dispatcher
