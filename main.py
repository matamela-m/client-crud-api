from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

clients = [
    {"id": 1, "name": "Jane Dlamini", "company": "Dlamini Consulting", "status": "lead", "project": "Website redesign"},
    {"id": 2, "name": "Sipho Khoza", "company": "Khoza Logistics", "status": "active", "project": "SEO retainer"},
    {"id": 3, "name": "Aisha Patel", "company": "Patel Interiors", "status": "completed", "project": "Portfolio site"},
]

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