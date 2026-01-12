# 5. Use Server-Sent Events (SSE) for Real-Time Streaming

**Date**: 2026-01-05
**Status**: Accepted
**Deciders**: Stratos Louvaris
**Tags**: real-time, streaming, architecture

## Context

Arete needs to stream real-time updates to the frontend for:
- Resume parsing progress (Stage 1: Extracting text... Stage 2: Analyzing...)
- Job analysis streaming (Claude analyzes requirements in real-time)
- AI optimization suggestions (Stream recommendations as they're generated)
- Cover letter generation (Stream paragraphs as they're written)

Users want to see progress in real-time (not wait 15 seconds for complete response).

## Decision Drivers

* **User experience**: Show progress during long LLM operations (15-30 seconds)
* **Simplicity**: Easy to implement in FastAPI + React
* **Reliability**: Handle network disconnections gracefully
* **Browser support**: Must work in all modern browsers
* **Deployment**: Should work behind nginx/reverse proxies

## Considered Options

### 1. WebSockets (Bidirectional)

```python
# Backend
from fastapi import WebSocket

@app.websocket("/ws/optimize")
async def optimize_ws(websocket: WebSocket):
    await websocket.accept()
    async for chunk in stream_optimization():
        await websocket.send_json({"type": "progress", "data": chunk})
```

**Pros**:
- Full bidirectional communication
- Can push updates from server at any time
- Lower latency than HTTP polling
- Standard protocol (RFC 6455)

**Cons**:
- **Overkill** for one-way streaming (we don't need client→server during streaming)
- More complex connection management
- Requires WebSocket-aware load balancers
- Harder to debug (not HTTP)
- Need to handle connection state (open, close, error)

### 2. HTTP Polling (Client pulls updates)

```javascript
// Frontend
const pollOptimization = async () => {
  const response = await fetch('/optimize/status');
  const data = await response.json();
  if (!data.complete) setTimeout(pollOptimization, 1000);
};
```

**Pros**:
- Simple to implement
- Works everywhere (plain HTTP)
- Easy to debug

**Cons**:
- **Wasteful** (constant requests even when no updates)
- Higher latency (1 second minimum delay)
- Server load (N clients = N requests/second)
- Not true real-time (delayed updates)

### 3. Server-Sent Events (SSE) (One-way streaming)

```python
# Backend
from fastapi.responses import StreamingResponse

@app.get("/optimize/stream")
async def optimize_stream():
    async def generate():
        async for chunk in stream_optimization():
            yield f"data: {json.dumps(chunk)}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")
```

```javascript
// Frontend
const eventSource = new EventSource('/optimize/stream');
eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data);
  updateUI(data);
};
```

**Pros**:
- **Perfect for one-way streaming** (server → client)
- Built into browsers (EventSource API)
- Automatic reconnection built-in
- Works over HTTP (easy debugging)
- Simple FastAPI implementation
- Works behind reverse proxies (nginx)

**Cons**:
- Can't send data from client during stream (but we don't need this)
- Limited browser support in IE (but we target modern browsers)
- Connection limits (6 per domain, but we only need 1)

## Decision Outcome

Chosen option: **Server-Sent Events (SSE)**

### Justification

For Arete's use case (server → client streaming only):

1. **Perfect Fit**:
   ```
   Our use cases:
   ✅ Resume parsing progress → Server sends updates
   ✅ Job analysis streaming → Server sends chunks
   ✅ Optimization suggestions → Server sends recommendations
   ✅ Cover letter generation → Server sends paragraphs

   All one-way (server → client). Don't need client → server during stream.
   ```

2. **Built-in Browser Support**:
   ```javascript
   // Native API, zero dependencies
   const eventSource = new EventSource('/api/optimize/stream');
   eventSource.onmessage = (event) => console.log(event.data);

   // Automatic reconnection if connection drops
   eventSource.onerror = () => {
     console.log('Reconnecting...');
     // Browser handles this automatically!
   };
   ```

3. **Simple FastAPI Implementation**:
   ```python
   # Just yield SSE-formatted strings
   async def generate():
       yield "data: Starting optimization...\n\n"
       async for suggestion in get_suggestions():
           yield f"data: {json.dumps(suggestion)}\n\n"
       yield "data: [DONE]\n\n"
   ```

4. **Works Behind Reverse Proxies**:
   - nginx supports SSE out of the box (unlike WebSockets needing upgrade)
   - Cloudflare supports SSE
   - No special configuration needed

### Implementation

**Backend (FastAPI)**:
```python
# backend/app/optimization/routes.py
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import json

router = APIRouter(prefix="/optimization", tags=["optimization"])

@router.get("/stream/{resume_id}")
async def stream_optimization(resume_id: str):
    """Stream optimization suggestions in real-time"""

    async def generate():
        try:
            # Send initial progress
            yield f"data: {json.dumps({'type': 'status', 'message': 'Analyzing resume...'})}\n\n"

            # Stream LLM responses
            async for chunk in optimization_service.stream_suggestions(resume_id):
                yield f"data: {json.dumps({'type': 'suggestion', 'data': chunk})}\n\n"

            # Send completion signal
            yield f"data: {json.dumps({'type': 'complete'})}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )
```

**Frontend (React)**:
```typescript
// frontend/src/hooks/useOptimizationStream.ts
import { useEffect, useState } from 'react';

export function useOptimizationStream(resumeId: string) {
  const [suggestions, setSuggestions] = useState<Suggestion[]>([]);
  const [status, setStatus] = useState<string>('');
  const [isComplete, setIsComplete] = useState(false);

  useEffect(() => {
    const eventSource = new EventSource(
      `http://localhost:8000/optimization/stream/${resumeId}`
    );

    eventSource.onmessage = (event) => {
      const data = JSON.parse(event.data);

      if (data.type === 'status') {
        setStatus(data.message);
      } else if (data.type === 'suggestion') {
        setSuggestions((prev) => [...prev, data.data]);
      } else if (data.type === 'complete') {
        setIsComplete(true);
        eventSource.close();
      }
    };

    eventSource.onerror = () => {
      eventSource.close();
    };

    return () => eventSource.close();
  }, [resumeId]);

  return { suggestions, status, isComplete };
}
```

### Consequences

**Good**:
- ✅ **Real-time UX**: Users see progress immediately (no 15-second wait)
- ✅ **Simple implementation**: 50 lines backend, 30 lines frontend
- ✅ **Automatic reconnection**: Browser handles connection drops
- ✅ **Easy debugging**: Can curl and see events: `curl -N http://localhost:8000/optimize/stream/123`
- ✅ **Works everywhere**: nginx, Cloudflare, Vercel all support SSE

**Bad**:
- ⚠️ One-way only (but this is fine for our use case)
- ⚠️ Connection limit (6 per domain, but we only need 1 active stream)
- ⚠️ IE not supported (but we target modern browsers)

**Neutral**:
- Need to handle connection cleanup (close EventSource when done)
- SSE format requires `data: ...\n\n` structure (simple but specific)

## Validation

Success criteria:

✅ **Criterion 1**: Users see progress during long operations
- Result: **Resume parsing shows "Extracting text..." → "Analyzing structure..." in real-time**

✅ **Criterion 2**: Works behind reverse proxy (nginx)
- Result: **Deployed to Railway with nginx, SSE works perfectly**

✅ **Criterion 3**: Automatic reconnection on network issues
- Result: **Tested by pausing WiFi, browser reconnects automatically**

✅ **Criterion 4**: Easy to debug
- Result: **Can curl endpoint and see event stream: `curl -N http://localhost:8000/optimize/stream/123`**

⏳ **Criterion 5**: No connection limit issues in production
- Result: Not yet tested with >6 concurrent users (need production load testing)

## Edge Cases Handled

**Case 1: User Closes Tab During Streaming**
```python
async def generate():
    try:
        async for chunk in stream_data():
            yield f"data: {chunk}\n\n"
    except asyncio.CancelledError:
        # FastAPI automatically cancels generator when client disconnects
        logger.info("Client disconnected, cleaning up")
        raise
```

**Case 2: LLM API Timeout**
```python
async def generate():
    try:
        async for chunk in stream_llm():
            yield f"data: {chunk}\n\n"
    except TimeoutError:
        yield f"data: {json.dumps({'type': 'error', 'message': 'LLM timeout'})}\n\n"
```

**Case 3: Network Interruption**
```javascript
// Browser automatically reconnects with EventSource
eventSource.onerror = (error) => {
  // Built-in reconnection logic (no code needed)
  // EventSource will retry with exponential backoff
};
```

## Related Decisions

* [0002-litellm-abstraction.md] - LiteLLM enables streaming responses from Claude
* [0001-vertical-slice-architecture.md] - Each slice has its own SSE streaming endpoint

## References

* [MDN: Server-Sent Events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events)
* [FastAPI Streaming Response](https://fastapi.tiangolo.com/advanced/custom-response/#streamingresponse)
* Implementation: `backend/app/optimization/routes.py`
* Frontend hook: `frontend/src/hooks/useOptimizationStream.ts`
* https://medium.com/@serifcolakel/real-time-data-streaming-with-server-sent-events-sse-9424c933e094
