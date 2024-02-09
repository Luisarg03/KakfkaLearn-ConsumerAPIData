import requests
import json
import uuid
from confluent_kafka import Producer
from datetime import datetime


# #########
# # CONFS #
# #########
TOPIC = 'used_cars'

with open(f'{TOPIC}.json') as f:
    topic_config = json.load(f)
f.close()

server_config = {
    'bootstrap.servers': 'localhost:9094'
}

producer = Producer(**server_config)


# ###############
# # HELP FUNCTS #
# ###############
def delivery_report(err, msg):
    if err is not None:
        print(f'Undelivered message: {err}')
    else:
        print(f'Message delivered {msg.topic()} / partition: [{msg.partition()}]')

    return None


# ###########
# # REQUEST #
# ###########
url = topic_config['url']
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
else:
    print("Error al realizar la solicitud:", response.status_code)

# ################
# # SEND MESSAGE #
# ################
attributes = topic_config['attributes']

data_filter = []
uuid = str(uuid.uuid1()).replace('-', '')[:12]

for d in data['results']:
    d = {attribute: d.get(attribute, None) for attribute in attributes}

    try:
        d['kfk_id'] = d['id'] + uuid
    except (Exception, KeyError) as e:
        e = e
        d['kfk_id'] = uuid

    d['kfk_timestamp'] = datetime.now().isoformat()

    d = json.dumps(d).encode('utf-8')
    producer.produce(TOPIC, d, callback=delivery_report)
    producer.poll(0)

producer.flush()
