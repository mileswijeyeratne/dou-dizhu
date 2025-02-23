from fastapi import FastAPI
from app.routes import test_route
from app.routes import websocket

app = FastAPI()

app.include_router(test_route.router)
app.include_router(websocket.router)