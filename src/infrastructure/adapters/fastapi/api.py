from fastapi import FastAPI

from src.infrastructure.adapters.db.database import Base, engine
from src.infrastructure.adapters.fastapi.routes import auth_routes, user_routes
from src.infrastructure.adapters.fastapi.swagger_info import API_DOCS

# Create all tables in the database
Base.metadata.create_all(bind=engine)

app = FastAPI(**API_DOCS["info"], openapi_tags=API_DOCS["tags"])

app.include_router(auth_routes.router, prefix="/auth", tags=["authentication"])
app.include_router(user_routes.router, prefix="/users", tags=["users"])


@app.get("/")
async def check_status_service():
    return {"status": "Is Running"}
