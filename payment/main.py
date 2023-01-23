from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.background import BackgroundTasks

from redis_om import get_redis_connection, HashModel
from starlette.requests import Request

import requests, time

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


class Order(HashModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str  # pending, completed, refunded

    class Meta:
        database = redis


@app.get("/orders")
async def get_all():
    return [await get(pk) for pk in Order.all_pks()]


@app.get("/orders/{pk}")
async def get(pk: str):
    return Order.get(pk)


@app.post("/orders")
async def create(request: Request, background_task: BackgroundTasks):
    body = await request.json()

    req = requests.get(f"http://localhost:9000/products/{body['id']}")
    product = req.json()

    order = Order(
        product_id=body["id"],
        price=product["price"],
        fee=0.2 * product["price"],
        total=1.2 * product["price"],
        quantity=body["quantity"],
        status="pending"
    )
    order.save()

    background_task.add_task(order_completed, order)

    return order


async def order_completed(order: Order):
    time.sleep(5)
    order.status = "completed"
    order.save()
    redis.xadd("order_completed", order.dict(), "*")
