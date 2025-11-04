from fastapi import FastAPI
from api import router as api_router
from kafka_config import consume_messages
from rabbitmq_config import consume_rabbitmq_messages
from contextlib import asynccontextmanager


@asynccontextmanager
async def LifeSpan(app: FastAPI):
    print("-----------------APP STARTED----------------------")
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, consume_rabbitmq_messages)
    loop.run_in_executor(None, consume_messages)
    yield
    print("-----------------APP ENDED----------------------")


app = FastAPI(
    title="Mail Service",
    version="1.0.0",
    description="Service for sending emails",
    summary="This API provides endpoints for sending emails.",
    lifespan=LifeSpan,
)

app.include_router(api_router, prefix="/api", tags=["Mail Service"])


@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Welcome to the Mail Service API"}
