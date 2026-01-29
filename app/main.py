from fastapi import FastAPI

from app.api.v1.api import api_router
from app.core.database import Base, engine

# DEV ONLY — remove in prod
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="User Management API",
    version="1.0.0",
)

# Infra / system endpoint
@app.get("/health", tags=["System"])
def health():
    return {"status": "ok"}

# Versioned APIs
app.include_router(
    api_router,
    prefix="/api/v1",
)

