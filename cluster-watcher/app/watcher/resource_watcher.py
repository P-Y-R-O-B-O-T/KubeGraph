import asyncio
from kubernetes import client ,watch
from typing import Dict,Optional
from app.dispatcher.event_dispatcher import EventDispatcher
from constants.config import WATCH_TIMEOUT_SECONDS
from utils.listmethods import get_list_method

class ResourceWatcher:
    """
    Watches a single Kubernetest resouce type in a cluster and dispatches it to 
    the respective qeueu using the EventProcessor.
    """
    
    def __init__(self,cluster_name:str,api_client:client.ApiClient,resource:str,dispatcher:EventDispatcher):
        self.cluster_name=cluster_name
        self.api_client=api_client
        self.resouce=resource
        self.dispatcher=dispatcher
        self.stop_event=asyncio.Event()
    
    def stop(self):
        self.stop_event.set()
        
    
    async def watch(self):
        w=watch.Watch()
        core_v1=client.CoreV1Api(api_client=self.api_clinet)
        
        while not self.stop_event.is_set():
            try:
                
                method = get_list_method(core_v1, self.resource)
                if method is None:
                    print(f"[WARN] Unsupported resource: {self.resource}")
                    return

              
                stream = await asyncio.to_thread(
                    lambda: w.stream(method, timeout_seconds=WATCH_TIMEOUT_SECONDS)
                )

                async for event in self._event_generator(stream):
                    if self.stop_event.is_set():
                        break
                    await self.dispatcher.publish_event(self.cluster_name, self.resource, event)

            except Exception as e:
                print(f"[ERROR] Watcher {self.cluster_name}:{self.resource} error: {e}")
                await asyncio.sleep(5)  
    
    
    async def _event_generator(self, stream):

        for event in stream:
            yield event
            
