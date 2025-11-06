import asyncio, json, websockets

async def main():
    uri = 'ws://127.0.0.1:8000/ws'
    async with websockets.connect(uri) as ws:
        await ws.send(json.dumps({'content':'hello from test'}))
        while True:
            msg = await ws.recv()
            print(msg)
            if json.loads(msg).get('type') == 'done':
                break

asyncio.run(main())
