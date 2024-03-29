from main import redis, Order
import time

key = 'refund_order'
group = 'payment-group'

try:
    redis.xgroup_create(key, group)
except Exception:
    print('Group already exists!')

while True:
    try:
        if results := redis.xreadgroup(group, key, {key: ">"}, None):
            print(results)
            for result in results:
                obj = result[1][0][1]
                order = Order.get(obj['pk'])
                order.status = 'refunded'
                order.save()

    except Exception as e:
        print(e)
    time.sleep(1)
