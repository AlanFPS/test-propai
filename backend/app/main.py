import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import httpx

from .config import SETTINGS
from .providers.factory import create_provider


app = FastAPI(title="AI Chat Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=SETTINGS.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def _ollama_available() -> bool:
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            resp = await client.get(f"{SETTINGS.ollama_host}/api/tags")
            return resp.status_code == 200
    except Exception:
        return False


@app.get("/health")
async def health() -> dict:
    return {
        "status": "ok",
        "ollama": await _ollama_available(),
        "model": SETTINGS.ollama_model,
    }


@app.websocket(SETTINGS.ws_path)
async def websocket_endpoint(ws: WebSocket) -> None:
    await ws.accept()
    try:
        while True:
            incoming = await ws.receive_text()
            try:
                data = json.loads(incoming)
            except Exception:
                await ws.send_json({"type": "error", "message": "invalid_json"})
                continue

            # Normalize payload into a messages list of {role, content}
            if isinstance(data, dict):
                messages = data.get("messages")
                if not messages:
                    content = data.get("content", "")
                    messages = [{"role": "user", "content": str(content)}]
            elif isinstance(data, list):
                if all(isinstance(it, dict) and "role" in it and "content" in it for it in data):
                    messages = data
                else:
                    messages = [{"role": "user", "content": json.dumps(data)}]
            else:
                messages = [{"role": "user", "content": str(data)}]

            # Validate non-empty content
            if not messages or not any((m.get("content") or "").strip() for m in messages):
                await ws.send_json({"type": "error", "message": "empty_payload"})
                continue

            provider = await create_provider()
            await ws.send_json({"type": "start", "provider": provider.name})

            try:
                async for token in provider.stream_chat(messages):
                    await ws.send_json({"type": "token", "content": token})
                await ws.send_json({"type": "done"})
            except Exception as e:
                await ws.send_json({"type": "error", "message": str(e)})
    except WebSocketDisconnect:
        return

