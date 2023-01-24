from main import redis, Product
import time

key = 'order_completed'
group = 'inventory-group'

try:
    redis.xgroup_create(key, group)
except:
    print('Group already exists!')

while True:
    try:
        if results := redis.xreadgroup(group, key, {key: ">"}, None):
            for result in results:
                obj = result[1][0][1]
                try:
                    product = Product.get(obj['product_id'])
                    product.quantity = product.quantity - int(obj['quantity'])
                    product.save()
                except Exception:
                    redis.xadd('refund_order', obj, '*')

    except Exception as e:
        print(str(e))
    time.sleep(1)