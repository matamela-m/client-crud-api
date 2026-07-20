# Client API

A CRUD API for managing clients, built with FastAPI and backed by a SQLite database. Data persists to disk, so clients survive server restarts. Models a basic agency workflow: leads, active clients, and completed projects.

## Install & run

```bash
python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && uvicorn main:app --reload
```

Server runs at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

On first run, the database is created and seeded automatically. No manual setup needed.

## Database

This project uses **SQLite**, chosen because:

- It's a single file (`clients.db`), no separate database server to install or run
- Zero setup: it ships with Python, nothing extra to configure
- Data survives restarts, unlike the in-memory version this project started as

The database file `clients.db` is created automatically in the project root the first time you start the server. It's git-ignored, so every fresh clone starts clean: the table is created and three example clients are seeded on first run.

## Endpoints

| Method | Path                    | Description                                    |
|--------|-------------------------|------------------------------------------------|
| GET    | /                       | API info                                       |
| GET    | /health                 | Health check                                   |
| GET    | /clients                | List all clients                               |
| GET    | /clients?status=active  | Filter clients by status                       |
| GET    | /clients?search=dlamini | Search clients by name or company              |
| GET    | /clients/{id}           | Get a single client by id                      |
| GET    | /stats                  | Counts of clients by status                    |
| POST   | /clients                | Create a client (name required)                |
| PUT    | /clients/{id}           | Update a client's fields                       |
| DELETE | /clients/{id}           | Delete a client                                |

## Client shape

```json
{
  "id": 1,
  "name": "Jane Dlamini",
  "company": "Dlamini Consulting",
  "status": "lead",
  "project": "Website redesign"
}
```

Status values used: `lead`, `active`, `completed`.

## Example

```
curl -i http://localhost:8000/clients/2
```
HTTP/1.1 200 OK
content-type: application/json
{"id":2,"name":"Sipho Khoza","company":"Khoza Logistics","status":"active","project":"SEO retainer"}

![Example 01](/images/example-01.png)

## Exploring the database directly

The database can be opened in DB Browser for SQLite. Example query run by hand:

```sql
SELECT * FROM clients WHERE status = 'active';
```

It returned only the clients whose status is "active", read straight from `clients.db`, the same file the API serves from. Changes made in DB Browser appear instantly through the API with no restart, proving the API and database share one source of truth.

## Screenshots

Swagger UI:

![Swagger UI 01](/images/swagger-ui-01.png)
![Swagger UI 01](/images/swagger-ui-02.png)

Database in DB Browser:

![DB Browser 01](/images/sqlite-database-01.png)