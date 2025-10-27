from fastapi import FastAPI
from model import RequestPayload, ResponsePayload
from kafka import KafkaProducer
from contextlib import asynccontextmanager
from decouple import config

@asynccontextmanager
async def fastapi_lifespan(app):
    # Run during application startup
    producer = KafkaProducer()
    await producer.init_connection()
    yield 
    # Run before application is stopped
    await producer.stop()

app = FastAPI(lifespan=fastapi_lifespan)

@app.post("/student", response_model=ResponsePayload)
async def create_student(body: RequestPayload):
    producer = KafkaProducer()
    acks = config("kafka_acks", cast=int)
    if acks == 0:
        result = await producer.push_message_with_zero_acks(body=body.model_dump(), key=body.id)
    else:
        result = await producer.push_message_with_one_acks(body=body.model_dump(), key=body.id)
    return ResponsePayload(status="Success", message=f"Message published successfully.")

