# Client API

A simple in-memory CRUD API for managing clients, built with FastAPI as a learning project. Models a basic agency workflow: leads, active clients, and completed projects.

## Install & run

```bash
python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && uvicorn main:app --reload
```

Server runs at `http://localhost:8000`. Interactive docs at `http://localhost:8000/docs`.

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

## Swagger UI

![Swagger UI 01](/images/swagger-ui-01.png)
![Swagger UI 02](/images/swagger-ui-02.png)