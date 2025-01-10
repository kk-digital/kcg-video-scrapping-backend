from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import psutil
import asyncio
from typing import List

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        disconnected_connections = []
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except RuntimeError:
                # Connection is already closed
                disconnected_connections.append(connection)
            except WebSocketDisconnect:
                disconnected_connections.append(connection)
        
        # Clean up disconnected connections
        for connection in disconnected_connections:
            self.disconnect(connection)

async def get_disk_space():
    '''
    Get disk space information for sending to clients
    '''
    disk = psutil.disk_usage('/')
    return {
        "type": "disk_space",
        "free": disk.free,
        "total": disk.total,
        "percent": disk.percent
    }

manager = ConnectionManager()

@router.websocket("/ws/downloads-status")
async def downloads_ws(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            disk_space = await get_disk_space()
            await manager.broadcast(disk_space)
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception:
        manager.disconnect(websocket)
