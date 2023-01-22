from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# This could be a different database
redis = get_redis_connection(
    host="redis-16843.c212.ap-south-1-1.ec2.cloud.redislabs.com",
    port=16843,
    password="oKGmt1TJvSDRffc4wPP9p0bkfUHUelQV",
    decode_responses=True
)

