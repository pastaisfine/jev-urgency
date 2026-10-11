# server.py
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

from jev_project.jev import score_urgency

INDEX = Path(__file__).parent / "index.html"


app = FastAPI()


class Req(BaseModel):
    transcript: str


@app.post("/score")
def score(req: Req):  # sync def runs in a threadpool, so urllib won't block the loop
    return score_urgency(req.transcript) or {"error": "jev call failed"}


@app.get("/")
def index():
    return FileResponse("index.html")
