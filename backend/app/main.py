from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.routes import websocket, auth, stats
from app.database import database

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.open_pool()

    yield

    await database.close_pool()

app = FastAPI(lifespan=lifespan)

app.include_router(websocket.router)
app.include_router(auth.router)
app.include_router(stats.router)