import json
import redis
from confluent_kafka import Consumer, KafkaError


# #########
# # CONFS #
# #########
TOPIC = 'used_cars'

config = {
    'bootstrap.servers': 'localhost:9094',
    'group.id': 'consumer_autos_usados',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(**config)
consumer.subscribe([TOPIC])

# Configuración de Redis
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 1
REDIS_PASSWORD = "my-password"

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    # password=REDIS_PASSWORD
)


try:
    while True:
        msg = consumer.poll(timeout=1.0)

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(msg.error())
                break

        # Extraer el ID del mensaje y el contenido
        message_data = json.loads(msg.value().decode('utf-8'))
        register_id = message_data['kfk_id']

        # Convertir el mensaje a una cadena JSON para almacenarlo en Redis
        message_str = json.dumps(message_data)

        redis_client.set(register_id, message_str)
        print(f"Mensaje almacenado en Redis con clave {register_id}: {message_str}")
        # register_id = json.loads(msg.value().decode('utf-8'))['kfk_id']
        # msg = msg.value().decode('utf-8')
        # print(msg)

        # replacements = {
        #     '{{{REGISTER_ID}}}': register_id,
        #     '{{{DATA}}}': msg,
        #     '{{{SCHEMA_NAME}}}': SCHEMA_NAME,
        #     '{{{TABLE_NAME}}}': TOPIC
        # }

finally:
    consumer.close()
