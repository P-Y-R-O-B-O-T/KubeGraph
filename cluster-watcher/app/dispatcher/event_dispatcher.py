from typing import Dict, Optional
import asyncio

from utils.messageBody import create_message, MessageBody

class EventDispatcher:
    def __init__(self):
        self.queues = {}

    def get_queue(self, cluster_name: str) -> asyncio.Queue:
        if cluster_name not in self.queues:
            self.queues[cluster_name] = asyncio.Queue()
        return self.queues[cluster_name]
    
    def get_all_queue(self):
        return self.queues


    async def dispatch_event(self, cluster_name: str, resource: str, event: Dict):
        message = create_message(resource, cluster_name, event=event)
        queue = self.get_queue(cluster_name)
        await queue.put(message)

    async def consume_events(self, cluster_name: str):
        queue = self.get_queue(cluster_name)
        while True:
            message = await queue.get()
            yield message
            
            print("Dispatching event:", message.get_body())
            queue.task_done()
            
            ###  Todo: Plan should we push to some queue for send for processing of this message.
            
