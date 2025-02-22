from fastapi import FastAPI
from app.routes import test_route

app = FastAPI()

app.include_router(test_route.router)