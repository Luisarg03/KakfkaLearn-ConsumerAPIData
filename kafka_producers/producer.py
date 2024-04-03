import os
import requests
import json
from confluent_kafka import Producer

from topics.cryptocoins_by_range.cryptocoins_by_range import cryptocoins_by_range


#########
# CONFS #
#########

server_config = {
    'bootstrap.servers': 'localhost:9094'
}

producer = Producer(**server_config)

TOPICS = {
    'cryptocoins_by_range': cryptocoins_by_range
}


# ###############
# # HELP FUNCTS #
# ###############
def read_all_json_files(folder_path):
    json_files = []
    for f1 in os.listdir(folder_path):
        if not f1.endswith('.py'):
            for f2 in os.listdir(f'{folder_path}/{f1}'):
                if f2.endswith('.json'):
                    file_path = os.path.join(folder_path, f1, f2)
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


def func_map(conf, func_mapping):
    topic_function = func_mapping.get(conf['topic'])
    if topic_function:
        return topic_function(conf)
    else:
        print(f"Function not found for topic {conf['topic']}")


# ##############
# # ITER FILES #
# ##############
folder_path = './topics/'
topic_configs = read_all_json_files(folder_path)

for conf in topic_configs:
    if conf['topic'] in TOPICS:
        data = func_map(conf, TOPICS)

        for d in data:
            topic = conf['topic']
            d = json.dumps(d).encode('utf-8')
            producer.produce(topic, d, callback=delivery_report)
            producer.poll(0)

        producer.flush()
