import uuid
import json
import requests as rqsts
from datetime import datetime
from confluent_kafka import Producer


class CommonKakfa:
    def __init__(self, conf):

        self.server_config = {
            'bootstrap.servers': 'localhost:9094'
        }

        self.producer = self.init_producer()
        self.topic = conf['topic']
        self.data = None

    def init_producer(self):
        return Producer(**self.server_config)

    def delivery_report(self, err, msg):
        if err is not None:
            print(f'Undelivered message: {err}')
        else:
            print(f'Message delivered {msg.topic()} / partition: [{msg.partition()}]')

        return None

    def kafka_produce(self, data):
        self.producer.produce(
            topic=self.topic,
            key=str(uuid.uuid4()),
            value=data,
            timestamp=int(datetime.now().timestamp()),
            callback=self.delivery_report
        )

        self.producer.flush()


class CommonClass:
    def __init__(self, conf):
        self.conf = conf

    def get_data(self):
        url = self.conf['url_format']

        for key, value in self.conf['attr'].items():
            url = url.replace(f'{{{{{key}}}}}', str(value))

        try:
            data = rqsts.get(url, timeout=10)
        except (
                rqsts.exceptions.RequestException,
                rqsts.exceptions.Timeout,
                rqsts.exceptions.ConnectionError
        ) as e:
            print(e)
            return None

        try:
            data = data.json()
        except json.JSONDecodeError as e:
            print(e)
            return None

        return data
