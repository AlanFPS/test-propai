from abc import ABC, abstractmethod
from typing import AsyncIterator, Dict, List


class ChatProvider(ABC):
    name: str = "base"

    @abstractmethod
    async def stream_chat(self, messages: List[Dict[str, str]]) -> AsyncIterator[str]:
        """Stream assistant tokens for the given chat messages."""
        raise NotImplementedError



