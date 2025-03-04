from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import List

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# List to store active WebSocket connections
active_connections: List[WebSocket] = []

@app.get("/")
def home():
    return {"message": "Tvara-Sockets is running!"}

@app.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str):
    await websocket.accept()
    active_connections.append(websocket)
    print(f"🔵 {username} connected.")

    try:
        while True:
            data = await websocket.receive_text()
            print(f"📩 {username}: {data}")
            
            # Broadcast message to all clients
            for connection in active_connections:
                await connection.send_text(f"{username}: {data}")

    except WebSocketDisconnect:
        print(f"🔴 {username} disconnected.")
        active_connections.remove(websocket)