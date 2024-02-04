import requests
import json
from confluent_kafka import Producer
from datetime import datetime


config = {
    'bootstrap.servers': 'localhost:9094'
}

producer = Producer(**config)


def delivery_report(err, msg):
    if err is not None:
        print(f'Mensaje no entregado: {err}')
    else:
        print(f'Mensaje entregado a {msg.topic()} [{msg.partition()}]')


url = "https://api.mercadolibre.com/sites/MLA/search?q=peugeot 208 gti&offset=0"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
else:
    print("Error al realizar la solicitud:", response.status_code)

attributes = [
    "id",
    "site_id",
    "category_id",
    "currency_id",
    "price",
    "original_price",
    "sale_price",
    "seller",
    "location",
    "timestamp"
]

data_filter = []
for d in data['results']:
    d['timestamp'] = datetime.now().isoformat()
    selected_attributes = {attribute: d.get(attribute, None) for attribute in attributes}
    message = json.dumps(selected_attributes).encode('utf-8')
    producer.produce('autos_usados', message, callback=delivery_report)
    producer.poll(0)

producer.flush()
