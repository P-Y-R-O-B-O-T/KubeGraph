import asyncio

from typing import List
from notifier.schemas import EventData
subscribers:List[asyncio.Queue]=[]

def subscribe_client()->asyncio.Queue:
    queue=asyncio.Queue()
    subscribers.append(queue)
    return queue

def unsubscribe_client(queue:asyncio.Queue):
    if queue in  subscribers:
        subscribers.remove(queue)

async def push_to_subscribers(event_data:EventData):
    for queue in subscribers:
        await queue.put(event_data)
        
