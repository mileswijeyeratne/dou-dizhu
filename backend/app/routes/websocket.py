from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()

# test echo server
@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    try:
        while True:
            data = await websocket.receive_text()
            print(data)
            await websocket.send_text(f"Message received: {data}")
    except WebSocketDisconnect:
        return
