from fastapi import APIRouter, Request
from fastapi import WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

from ..dependecies import templates, ws_manager


router = APIRouter()


@router.get("/ws", response_class=HTMLResponse)
async def get(request: Request):
    return templates.TemplateResponse("ws.html", {"request": request})


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await ws_manager.connect(client_id, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(client_id)