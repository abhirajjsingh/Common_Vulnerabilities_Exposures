from fastapi import FastAPI
from .database import db
from .routes import cve
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="CVE Dashboard API")

# Include routers
app.include_router(cve.router, prefix="/api/cves", tags=["cves"])

@app.on_event("startup")
async def startup_event():
    await db.connect_to_mongodb()

@app.on_event("shutdown")
async def shutdown_event():
    await db.close_mongodb_connection()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)