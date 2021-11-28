from fastapi import WebSocket


class ConnectionManager:
    connections: dict[int: WebSocket]

    def __init__(self):
        self.connections = {}

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        self.connections[user_id] = websocket

    def disconnect(self, user_id: int):
        self.connections.pop(user_id)

    async def send_personal_message(self, message: str, user_id: int):
        await self.connections[user_id].send_json({'text': message})

    async def send_personal_json(self, data: dict, user_id: int):
        await self.connections[user_id].send_json(data)

    async def broadcast(self, message: str):
        for connection in self.connections.values():
            await connection.send_text(message)
