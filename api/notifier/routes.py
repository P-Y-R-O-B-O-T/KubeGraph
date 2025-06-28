
import queue
from fastapi import APIRouter ,Depends,HTTPException,status,Query,Request
from fastapi.responses import StreamingResponse
from authentication.auth import get_current_active_user
from authentication.schemas import User
from typing import Annotated,Optional
import json
from notifier.methods import subscribe_client,push_to_subscribers,unsubscribe_client
from notifier.schemas import EventData

NOTIFIER_ROUTER=APIRouter(prefix="/notifier",tags=["notifier"])

@NOTIFIER_ROUTER.get("/events") ## this could be called by frontend.
async def sse_events(
    request:Request,
    current_user: Annotated[User, Depends(get_current_active_user)],
    event_type:Optional[str]=Query(None),
    event_id:Optional[str]=Query(None),
):
    queue=subscribe_client()
    

    async def event_stream():
        try:
            while True:
                if await request.is_disconnected():
                    break
                event=await queue.get()
                yield f"data:{event}\n\n"
            
        finally:
            unsubscribe_client(queue=queue)
            
    return StreamingResponse(event_stream(),media_type="text/event-stream")

    
@NOTIFIER_ROUTER.post("/update") # this would be called by the cluster watcher 
async def notify_client(
    payload:EventData,
    # current_user: Annotated[User, Depends(get_current_active_user)],
):
    await push_to_subscribers(payload)
    return {"status": "notified", "notified_at": payload.timestamp.isoformat()}

