import os
from typing import List


class Settings:
    def __init__(self) -> None:
        self.ollama_host: str = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.ollama_model: str = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
        cors_origins_env = os.getenv("CORS_ORIGINS", "http://localhost:5173")
        self.cors_origins: List[str] = [o.strip() for o in cors_origins_env.split(",") if o.strip()]
        self.ws_path: str = os.getenv("WS_PATH", "/ws")


SETTINGS = Settings()



