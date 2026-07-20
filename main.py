from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

clients = [
    {"id": 1, "name": "Jane Dlamini", "company": "Dlamini Consulting", "status": "lead", "project": "Website redesign"},
    {"id": 2, "name": "Sipho Khoza", "company": "Khoza Logistics", "status": "active", "project": "SEO retainer"},
    {"id": 3, "name": "Aisha Patel", "company": "Patel Interiors", "status": "completed", "project": "Portfolio site"},
]


class ClientCreate(BaseModel):
    name: Optional[str] = None
    company: Optional[str] = None
    status: Optional[str] = None
    project: Optional[str] = None


@app.get("/")
def read_root():
    return {
        "name": "Client API",
        "version": "1.0",
        "endpoints": ["/clients"]
    }


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/clients")
def get_clients():
    return clients


@app.get("/clients/{client_id}")
def get_client(client_id: int):
    for client in clients:
        if client["id"] == client_id:
            return client
    return JSONResponse(
        status_code=404,
        content={"error": f"Client {client_id} not found"}
    )


@app.post("/clients")
def create_client(client: ClientCreate):
    if not client.name or not client.name.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "name is required and cannot be empty"}
        )

    next_id = max((c["id"] for c in clients), default=0) + 1
    new_client = {
        "id": next_id,
        "name": client.name,
        "company": client.company or "",
        "status": client.status or "lead",
        "project": client.project or "",
    }
    clients.append(new_client)

    return JSONResponse(status_code=201, content=new_client)