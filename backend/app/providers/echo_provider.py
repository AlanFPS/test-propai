import asyncio
from typing import AsyncIterator, Dict, List

from .base import ChatProvider


class EchoProvider(ChatProvider):
    name = "echo"

    async def stream_chat(self, messages: List[Dict[str, str]]) -> AsyncIterator[str]:
        # Find latest user message
        user_content = ""
        for m in reversed(messages):
            if m.get("role") == "user":
                user_content = m.get("content", "")
                break
        text = f"Echo: {user_content}" if user_content else "Echo: Hello!"
        # Stream in small chunks
        chunk_size = 6
        for i in range(0, len(text), chunk_size):
            yield text[i : i + chunk_size]
            await asyncio.sleep(0.02)



