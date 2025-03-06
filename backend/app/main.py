from fastapi import FastAPI
from app.routes import websocket

app = FastAPI()

app.include_router(websocket.router)