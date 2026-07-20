from fastapi import FastAPI

app = FastAPI()

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