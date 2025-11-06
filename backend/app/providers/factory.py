import httpx
from typing import Optional

from ..config import SETTINGS
from .base import ChatProvider
from .echo_provider import EchoProvider


async def _ollama_available() -> bool:
    try:
        async with httpx.AsyncClient(timeout=3.0) as client:
            resp = await client.get(f"{SETTINGS.ollama_host}/api/tags")
            return resp.status_code == 200
    except Exception:
        return False


async def create_provider() -> ChatProvider:
    # Lazy import to avoid optional dependency at startup
    if await _ollama_available():
        from .ollama_provider import OllamaChatProvider

        return OllamaChatProvider(SETTINGS.ollama_host, SETTINGS.ollama_model)
    return EchoProvider()



