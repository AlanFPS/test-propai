import json
from typing import AsyncIterator, Dict, List

import httpx

from .base import ChatProvider


class OllamaChatProvider(ChatProvider):
    name = "ollama"

    def __init__(self, host: str, model: str) -> None:
        self.host = host.rstrip("/")
        self.model = model

    async def stream_chat(self, messages: List[Dict[str, str]]) -> AsyncIterator[str]:
        url = f"{self.host}/api/chat"
        payload = {"model": self.model, "messages": messages, "stream": True}
        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream("POST", url, json=payload) as resp:
                resp.raise_for_status()
                async for line in resp.aiter_lines():
                    if not line:
                        continue
                    try:
                        data = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    # Ollama chat stream typically provides incremental message content
                    message = data.get("message")
                    if message and isinstance(message, dict):
                        piece = message.get("content")
                        if piece:
                            yield piece
                            continue
                    # Fallback for generate stream shape
                    piece = data.get("response")
                    if piece:
                        yield piece



