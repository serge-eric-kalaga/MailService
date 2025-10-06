from fastapi import FastAPI
import uvicorn
from api import router as api_router


app = FastAPI(
    title="Mail Service",
    version="1.0.0",
    description="Service for sending emails",
    summary="This API provides endpoints for sending emails.",
)

app.include_router(api_router, prefix="/api", tags=["Mail Service"])


@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Welcome to the Mail Service API"}
