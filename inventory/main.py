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

redis = get_redis_connection(
    host="redis-16843.c212.ap-south-1-1.ec2.cloud.redislabs.com",
    port=16843,
    password="oKGmt1TJvSDRffc4wPP9p0bkfUHUelQV",
    decode_responses=True
)


class Product(HashModel):
    name: str
    price: int
    quantity: int

    class Meta:
        database = redis


@app.get("/products")
async def all():
    return [await format(pk) for pk in Product.all_pks()]


async def format(pk: str):
    product = Product.get(pk)

    return {
        "id": product.pk,
        "name": product.name,
        "price": product.price,
        "quantity": product.quantity
    }


@app.post("/products")
async def create(product: Product):
    return product.save()


@app.get("/products/{pk}")
async def get(pk: str):
    return Product.get(pk)


@app.delete("/products/{pk}")
async def delete(pk: str):
    return Product.delete(pk)


@app.put("/products/{pk}")
async def update(pk: str):
    return Product.update(pk)
