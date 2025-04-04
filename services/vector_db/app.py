import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from db import init_db, query_db
import logging
app = FastAPI()

collection = None

logging.basicConfig(level=logging.INFO)
@app.on_event("startup")
def startup_event():
    logging.info("Initializing database")
    global collection
    collection = init_db()
    logging.info("Database initialized")

class AddRequest(BaseModel):
    text_chunk: str

class QueryRequest(BaseModel):
    query: str
    k: int

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/add")
def add_to_db_endpoint(request: AddRequest):
    if not collection:
        logging.error("Database not initialized")
        raise HTTPException(status_code=500, detail="Database not initialized")
    
    collection.add(documents=[request.text_chunk], ids=[str(uuid.uuid4())])
    return {"status": "success", "message": "Document added successfully"}

@app.get("/query")
def query_db_endpoint(request: QueryRequest):
    if not collection:
        raise HTTPException(status_code=500, detail="Database not initialized")
    results = query_db(collection, request.query, request.k)
    return {"results": results}