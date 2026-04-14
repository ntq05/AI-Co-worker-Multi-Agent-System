from fastapi import FastAPI
from app.api.routes import chat

app = FastAPI(title = "AI Company Simulation")

app.include_router(chat.router, prefix="/api")