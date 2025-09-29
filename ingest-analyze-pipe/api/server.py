#!/usr/bin/env python3
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
import os, json, pathlib

app = FastAPI(title="Music-AI API")

JOBS = {}
OUT_DIR = os.getenv("OUT_DIR","tmp/final")

class JobRequest(BaseModel):
    source_url: str
    id: str | None = None

@app.post("/jobs", status_code=202)
def submit_job(req: JobRequest):
    job_id = req.id or f"job_{len(JOBS)+1}"
    JOBS[job_id] = {"status":"queued","source_url": req.source_url}
    # In production: publish to Pub/Sub; here we just mock status.
    return {"id": job_id, "status": "queued"}

@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    job = JOBS.get(job_id)
    if not job:
        raise HTTPException(404, "not found")
    return job

@app.get("/maps/{job_id}")
def get_map(job_id: str):
    path = pathlib.Path(OUT_DIR)/f"{job_id}.song_map.json"
    if not path.exists():
        raise HTTPException(404, "not ready")
    return FileResponse(str(path), media_type="application/json")
