from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .core import settings

app = FastAPI(
    title="Storer API",
    version=settings.release_version,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/ping")
def ping():
    return {"ping": "pong"}
