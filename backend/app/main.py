from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.routes import websocket, auth, stats
from app.database import database

@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.open_pool()

    yield

    await database.close_pool()

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:8080",
    # "http://192.168.0.101:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(websocket.router)
app.include_router(auth.router)
app.include_router(stats.router)