from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import sqlite3

DB_NAME = "clients.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            company TEXT,
            status TEXT,
            project TEXT
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM clients")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.executemany(
            "INSERT INTO clients (name, company, status, project) VALUES (?, ?, ?, ?)",
            [
                ("Jane Dlamini", "Dlamini Consulting", "lead", "Website redesign"),
                ("Sipho Khoza", "Khoza Logistics", "active", "SEO retainer"),
                ("Aisha Patel", "Patel Interiors", "completed", "Portfolio site"),
            ]
        )

    conn.commit()
    conn.close()


app = FastAPI(
    title="Client API",
    description="A simple client management API built for learning.",
    version="1.0"
)

init_db()


class ClientCreate(BaseModel):
    name: Optional[str] = None
    company: Optional[str] = None
    status: Optional[str] = None
    project: Optional[str] = None


class ClientUpdate(BaseModel):
    name: Optional[str] = None
    company: Optional[str] = None
    status: Optional[str] = None
    project: Optional[str] = None


@app.get("/")
def read_root():
    """Returns basic info about this API and its available endpoints."""
    return {
        "name": "Client API",
        "version": "1.0",
        "endpoints": ["/clients"]
    }


@app.get("/health")
def health_check():
    """Health check endpoint used to confirm the server is running."""
    return {"status": "ok"}


@app.get("/clients")
def get_clients(status: Optional[str] = None, search: Optional[str] = None):
    """Returns clients, optionally filtered by status and/or a search term in the name or company."""
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM clients"
    params = []
    conditions = []

    if status is not None:
        conditions.append("status = ?")
        params.append(status)

    if search is not None:
        conditions.append("(LOWER(name) LIKE ? OR LOWER(company) LIKE ?)")
        term = f"%{search.lower()}%"
        params.append(term)
        params.append(term)

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


@app.get("/clients/{client_id}")
def get_client(client_id: int):
    """Returns a single client by id, or a 404 error if it doesn't exist."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM clients WHERE id = ?", (client_id,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return JSONResponse(
            status_code=404,
            content={"error": "Client not found"}
        )

    return dict(row)


@app.get("/stats")
def get_stats():
    """Returns a count of clients grouped by status."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM clients")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT status, COUNT(*) FROM clients GROUP BY status")
    by_status = {row[0]: row[1] for row in cursor.fetchall()}
    conn.close()

    return {
        "total": total,
        "leads": by_status.get("lead", 0),
        "active": by_status.get("active", 0),
        "completed": by_status.get("completed", 0),
    }


@app.post("/clients")
def create_client(client: ClientCreate):
    """Creates a new client from a name and returns it with a generated id."""
    if not client.name or not client.name.strip():
        return JSONResponse(
            status_code=400,
            content={"error": "name is required and cannot be empty"}
        )

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO clients (name, company, status, project) VALUES (?, ?, ?, ?)",
        (
            client.name,
            client.company or "",
            client.status or "lead",
            client.project or "",
        )
    )
    conn.commit()

    new_id = cursor.lastrowid

    cursor.execute("SELECT * FROM clients WHERE id = ?", (new_id,))
    row = cursor.fetchone()
    conn.close()

    return JSONResponse(status_code=201, content=dict(row))


@app.put("/clients/{client_id}")
def update_client(client_id: int, update: ClientUpdate):
    """Updates a client's fields. Fields not sent are left unchanged."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM clients WHERE id = ?", (client_id,))
    row = cursor.fetchone()

    if row is None:
        conn.close()
        return JSONResponse(
            status_code=404,
            content={"error": "Client not found"}
        )

    if update.name is not None and not update.name.strip():
        conn.close()
        return JSONResponse(
            status_code=400,
            content={"error": "name cannot be empty"}
        )

    current = dict(row)
    new_name = update.name if update.name is not None else current["name"]
    new_company = update.company if update.company is not None else current["company"]
    new_status = update.status if update.status is not None else current["status"]
    new_project = update.project if update.project is not None else current["project"]

    cursor.execute(
        "UPDATE clients SET name = ?, company = ?, status = ?, project = ? WHERE id = ?",
        (new_name, new_company, new_status, new_project, client_id)
    )
    conn.commit()

    cursor.execute("SELECT * FROM clients WHERE id = ?", (client_id,))
    updated = cursor.fetchone()
    conn.close()

    return dict(updated)


@app.delete("/clients/{client_id}")
def delete_client(client_id: int):
    """Deletes a client by id. Returns 204 with no body on success."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM clients WHERE id = ?", (client_id,))
    row = cursor.fetchone()

    if row is None:
        conn.close()
        return JSONResponse(
            status_code=404,
            content={"error": "Client not found"}
        )

    cursor.execute("DELETE FROM clients WHERE id = ?", (client_id,))
    conn.commit()
    conn.close()

    return JSONResponse(status_code=204, content=None)