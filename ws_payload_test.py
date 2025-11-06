import asyncio, json, websockets

TESTS = [
    ("string", json.dumps("hello")),
    ("number", json.dumps(123)),
    ("null", json.dumps(None)),
    ("empty_list", json.dumps([])),
    ("list_mixed", json.dumps(["a", 1])),
    ("list_messages", json.dumps([{ "role": "user", "content": "hi"}])),
    ("empty_object", json.dumps({})),
]

async def run_one(name, payload):
    uri = 'ws://127.0.0.1:8000/ws'
    async with websockets.connect(uri) as ws:
        await ws.send(payload)
        print(f"\n-- {name} -- sent: {payload}")
        while True:
            recv = await ws.recv()
            print(recv)
            try:
                msg = json.loads(recv)
            except Exception:
                break
            if msg.get('type') in ('done','error'):
                break

async def main():
    for name, payload in TESTS:
        await run_one(name, payload)

asyncio.run(main())
