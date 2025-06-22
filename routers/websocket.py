from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from typing import Dict
from utils.auth import verify_token  # 🔐 Token verification utility

router = APIRouter()

# 🔌 Dictionary to store active WebSocket connections: {user_id: WebSocket}
active_connections: Dict[int, WebSocket] = {}


@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int, token: str = Query(...)):
    try:
        verified_user = verify_token(token)
    except Exception as e:
        await websocket.close(code=1008)
        print(f"❌ Invalid token format: {e}")
        return

    # 🛡️ Ensure token's user ID matches path user_id
    if not verified_user or int(verified_user) != user_id:
        await websocket.close(code=1008)  # Policy Violation
        print(f"❌ Unauthorized WebSocket attempt for user {user_id}")
        return

    await websocket.accept()
    active_connections[user_id] = websocket
    print(f"✅ WebSocket connected: User {user_id}")

    try:
        while True:
            await websocket.receive_text()  # Keep the connection alive
    except WebSocketDisconnect:
        print(f"❌ WebSocket disconnected: User {user_id}")
    finally:
        if user_id in active_connections:
            del active_connections[user_id]
