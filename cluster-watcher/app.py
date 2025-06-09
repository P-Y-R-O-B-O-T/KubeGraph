import asyncio
import signal
from  app.watch_manager import WatcherManager


async def main():
    manager = WatcherManager()

   
    watcher_task = asyncio.create_task(manager.start())

        ## [Omkar:] here for testing we are printing the content , later we will  push to service that 
        ## can handle and work on this data.
        
    async def print_events():
        dispatcher = manager.get_dispatcher()
        queues = dispatcher.get_all_queues()

        tasks = []
        for cluster_name, queue in queues.items():
            async def consume(cluster=cluster_name, q=queue):
                while True:
                    event = await q.get()
                    print(f"[{cluster}] >> {event.get('type')} - {event.get('object').metadata.name}")
                    q.task_done()

            tasks.append(asyncio.create_task(consume()))

        await asyncio.gather(*tasks)

    # Start the event printer
    printer_task = asyncio.create_task(print_events())

    # Graceful shutdown
    stop_event = asyncio.Event()

    def handle_shutdown():
        print("\n[INFO] Received shutdown...")
        stop_event.set()

    signal.signal(signal.SIGINT, lambda *_: handle_shutdown())
    signal.signal(signal.SIGTERM, lambda *_: handle_shutdown())

    await stop_event.wait()
    await manager.stop()
    print("Shutdown completed")

if __name__ == "__main__":
    asyncio.run(main())
