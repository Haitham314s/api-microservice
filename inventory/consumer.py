from inventory.main import redis, Product

key = "order_completed"
group = "inventory-group"

try:
    redis.xgroup_create(key, group)
except:
    print("Group already exist")

while True:
    try:
        results = redis.xreadgroup(group, key, {key: ">"}, None)

        print()
    except Exception as e:
        print(str(e))
    time.sleep(1)
