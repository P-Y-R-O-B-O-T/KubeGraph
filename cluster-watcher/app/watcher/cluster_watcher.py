import asyncio
from typing import List
from kubernetes import client
from app.watcher.resource_watcher import ResourceWatcher
from app.dispatcher.event_dispatcher import EventDispatcher

class ClusterWatcher:
    """
    The main method  for multiple resources on a single cluster.
    
    """
    
    
    def __init__(self, cluster_name: str, api_client: client.ApiClient, resources: List[str], dispatcher: EventDispatcher):
        self.cluster_name = cluster_name
        self.api_client = api_client
        self.resources = resources
        self.dispatcher = dispatcher
        self.watchers = []
        self.tasks = []
        
    
    
    async def start(self):
        for resource in self.resources:
            watcher = ResourceWatcher(self.cluster_name, self.api_client, resource, self.dispatcher)
            self.watchers.append(watcher)
            task = asyncio.create_task(watcher.watch())
            self.tasks.append(task)
    
    
    
    async def stop(self):
        for watcher in self.watchers:
            watcher.stop()
        await asyncio.gather(*self.tasks, return_exceptions=True)

