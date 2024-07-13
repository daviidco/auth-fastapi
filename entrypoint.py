import uvicorn

from src.infrastructure.adapters.fastapi.api import app

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8080)
