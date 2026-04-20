from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.api.deps import get_current_user
from app.services import vm as vm_service
import json
import asyncio

router = APIRouter()

# Менеджер для управления активными WS-соединениями
class ConnectionManager:
    def __init__(self):
        # Храним соединения в виде {user_id: websocket}
        self.active_connections: dict[int, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: int):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def send_personal_message(self, message: dict, user_id: int):
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_text(json.dumps(message))

manager = ConnectionManager()

@router.websocket("/ws/{token}")
async def websocket_endpoint(websocket: WebSocket, token: str, db: AsyncSession = Depends(get_db)):
    # 1. Проверка токена (т.к. заголовки в WS передать сложно, передаем токен в URL)
    from jose import jwt, JWTError
    from app.core.config import settings
    from app.services import user as user_service

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        user = await user_service.get_user_by_email(db, email)
        if not user:
            await websocket.close(code=1008)
            return
    except JWTError:
        await websocket.close(code=1008)
        return

    # 2. Принимаем соединение
    user_id = user.id
    await manager.connect(websocket, user_id)
    
    try:
        # 3. При подключении сразу отправляем текущий статус прокси
        from app.models.models import VirtualMachine
        from sqlalchemy import select
        
        vm_query = await db.execute(
            select(VirtualMachine).where(VirtualMachine.current_user_id == user_id)
        )
        vm = vm_query.scalars().first()
        
        status = "connected" if vm and vm.is_active else "no_proxy"
        await manager.send_personal_message({"type": "status", "status": status}, user_id)

        # 4. Цикл ожидания (keep-alive)
        while True:
            # Ждем данных от клиента (если нужно) или просто держим связь
            data = await websocket.receive_text()
            # Можно добавить логику обработки входящих команд от десктопа
            
    except WebSocketDisconnect:
        manager.disconnect(user_id)