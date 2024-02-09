import redis

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 1

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
keys = redis_client.keys('*')

for key in keys:
    value = redis_client.get(key)
    print(f"Clave: {key.decode('utf-8')}, Valor: {value.decode('utf-8')}")
