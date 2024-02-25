import os
import requests
import json
import uuid
from confluent_kafka import Producer
from datetime import datetime


#########
# CONFS #
#########

server_config = {
    'bootstrap.servers': 'localhost:9094'
}

producer = Producer(**server_config)


# ###############
# # HELP FUNCTS #
# ###############
def read_all_json_files(folder_path):
    json_files = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.json'):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path) as f:
                json_data = json.load(f)
                json_files.append(json_data)
    return json_files


def delivery_report(err, msg):
    if err is not None:
        print(f'Undelivered message: {err}')
    else:
        print(f'Message delivered {msg.topic()} / partition: [{msg.partition()}]')

    return None


# ##############
# # ITER FILES #
# ##############
folder_path = './topics'
topic_configs = read_all_json_files(folder_path)

for conf in topic_configs:
    # # REQUEST #
    url = conf['url']
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
    else:
        print("Bad request:", response.status_code)

    # # SEND MESSAGE #
    topic = conf['topic']
    parse_by = conf['parse_by']
    attributes = conf['attributes']

    id = uuid.uuid1()
    id = str(id).replace('-', '')[:12]

    try:
        data = data[parse_by]
    except (Exception, TypeError) as e:
        e = e
        data = data

    for d in data:
        try:
            d['kfk_id'] = d['id'] + id
        except (Exception, KeyError) as e:
            e = e
            d['kfk_id'] = uuid

        d['kfk_timestamp'] = datetime.now().isoformat()
        d = json.dumps(d).encode('utf-8')
        producer.produce(topic, d, callback=delivery_report)
        producer.poll(0)

    producer.flush()
