import { useEffect, useMemo, useRef, useState } from 'react'

type Message = { role: 'user' | 'assistant'; content: string }

function useWebSocket(url: string, onMessage: (data: any) => void) {
  const socketRef = useRef<WebSocket | null>(null)
  const callbackRef = useRef(onMessage)

  // Keep latest callback without retriggering connection
  useEffect(() => {
    callbackRef.current = onMessage
  }, [onMessage])

  useEffect(() => {
    let isMounted = true
    function connect() {
      const ws = new WebSocket(url)
      socketRef.current = ws
      ws.onmessage = (evt) => {
        try {
          const data = JSON.parse(evt.data)
          callbackRef.current(data)
        } catch {
          // ignore non JSON
        }
      }
      ws.onclose = () => {
        if (isMounted) setTimeout(connect, 1000)
      }
    }
    connect()
    return () => {
      isMounted = false
      socketRef.current?.close()
    }
  }, [url])

  return socketRef
}

export default function App() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [isStreaming, setIsStreaming] = useState(false)
  const wsUrl = useMemo(
    () => (import.meta.env.VITE_WS_URL as string) || 'ws://localhost:8000/ws',
    []
  )

  const onWsMessage = (data: any) => {
    if (data?.type === 'start') {
      setIsStreaming(true)
      setMessages((prev) => [...prev, { role: 'assistant', content: '' }])
    } else if (data?.type === 'token') {
      setMessages((prev) => {
        const copy = [...prev]
        const idx = copy.length - 1
        if (idx >= 0 && copy[idx].role === 'assistant') {
          copy[idx] = { role: 'assistant', content: copy[idx].content + (data.content || '') }
        }
        return copy
      })
    } else if (data?.type === 'done') {
      setIsStreaming(false)
    } else if (data?.type === 'error') {
      setIsStreaming(false)
      setMessages((prev) => [...prev, { role: 'assistant', content: `Error: ${data.message}` }])
    }
  }

  const socketRef = useWebSocket(wsUrl, onWsMessage)

  const sendMessage = () => {
    const text = input.trim()
    if (!text || !socketRef.current) return
    const ws = socketRef.current
    const userMsg: Message = { role: 'user', content: text }
    setMessages((prev) => [...prev, userMsg])
    const payload = JSON.stringify({ content: userMsg.content })
    if (ws.readyState === WebSocket.OPEN) {
      ws.send(payload)
    } else if (ws.readyState === WebSocket.CONNECTING) {
      const onOpen = () => {
        ws.send(payload)
        ws.removeEventListener('open', onOpen)
      }
      ws.addEventListener('open', onOpen)
    }
    setInput('')
  }

  return (
    <div className="app">
      <div className="chat">
        {messages.map((m, i) => (
          <div key={i} className={m.role === 'user' ? 'msg user' : 'msg assistant'}>
            {m.content}
          </div>
        ))}
      </div>
      <div className="inputBar">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' ? sendMessage() : null}
          placeholder="Type a message"
          disabled={isStreaming}
        />
        <button onClick={sendMessage} disabled={isStreaming || !input.trim()}>Send</button>
      </div>
      <div className="status">{isStreaming ? 'Streaming...' : 'Idle'}</div>
    </div>
  )
}



