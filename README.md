# AI Chat, FastAPI and React

FastAPI backend with WebSocket streaming and a minimal React client. Prefers Ollama locally, falls back to Echo.

## Backend

1. Create a virtual environment and install requirements

```bash
cd backend
pip install -r requirements.txt
```

2. Run the server

```bash
uvicorn app.main:app --reload --port 8000
```

Install & run Ollama locally

```bash
winget install Ollama.Ollama
```

Pull a small model

```bash
ollama pull llama3.2:3b
```

## Frontend

```bash
cd frontend
npm i
npm run dev
```

Open `http://localhost:5173`.

## Configuration

- WebSocket URL, `VITE_WS_URL` in the frontend, default `ws://localhost:8000/ws`
- Ollama host, `OLLAMA_HOST`, default `http://localhost:11434`
- Ollama model, `OLLAMA_MODEL`, default `llama3.2:3b`
