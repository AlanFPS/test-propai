# AI Chat, FastAPI and React

FastAPI backend with WebSocket streaming and a minimal React client. Prefers Ollama locally, falls back to Echo.

## Backend

1. Create virtual environment and install requirements

```bash
cd backend
pip install -r requirements.txt
```

2. Run the server

- From backend directory

```bash
py -m uvicorn app.main:app --reload --port 8000
```

3. Verify

```bash
curl http://127.0.0.1:8000/health
# {"status":"ok","ollama":false,"model":"llama3.2:3b"}
```

## Install and run Ollama

1. Install on Windowshell

```bash
winget install Ollama.Ollama
```

2. Pull a small model

```bash
ollama pull llama3.2:3b
```

3. Verify Ollama is up

```bash
ollama list
ollama serve # if shows “Only one usage of each socket address”, the service is already running.
```

Restart backend to pick up Ollama

```bash
py -m uvicorn app.main:app --reload --port 8000 --app-dir backend
curl http://127.0.0.1:8000/health # expect "ollama": true
```

## Configuration

- OLLAMA_HOST, default http://localhost:11434
- OLLAMA_MODEL, default llama3.2:3b
- CORS_ORIGINS, default http://localhost:5173
- WS_PATH, default /ws
- Frontend, VITE_WS_URL, default ws://localhost:8000/ws

## WebSocket payloads accepted

- Object with content

```bash
{"content": "hello"}
```

- Object with messages

```bash
{"messages":[{"role":"user","content":"hello"}]}
```

- Primitive, string or number or null

```bash
"hello"
```

- Array of messages, used directly

```bash
[{"role":"user","content":"hi"}]
```

- Empty array or empty object yields error event

```bash
[]
```
