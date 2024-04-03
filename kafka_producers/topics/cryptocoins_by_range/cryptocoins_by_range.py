import uuid
import json
import requests
from datetime import datetime


def cryptocoins_by_range(conf: dict) -> list:
    # # REQUEST #
    topic = conf['topic']
    url = conf['url']

    to = datetime.fromisoformat(datetime.now().isoformat())
    to = int(to.timestamp())

    replacements = {
        '{{{COIN}}}': conf['attr']['COIN'],
        '{{{CURRENCY}}}': conf['attr']['CURRENCY'],
        '{{{from}}}': conf['FROM'],
        '{{{to}}}': to
    }

    for old_value, new_value in replacements.items():
        url = url.replace(old_value, str(new_value))

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
    else:
        print("Bad request:", response.status_code)

    json_data = []

    for d in data['prices']:
        unix_timestamp = d[0] / 1000
        normal_date = datetime.utcfromtimestamp(unix_timestamp)

        id = uuid.uuid1()
        id = str(id).replace('-', '')

        d = {
            'coin': conf['attr']['COIN'],
            'date': normal_date.isoformat(),
            'currency': conf['attr']['CURRENCY'],
            'price': d[1],
            'kfk_timestamp': datetime.now().isoformat(),
            'kfk_id': id
        }

        json_data.append(d)

    if conf['json_update']:
        try:
            last_updated = max(d['date'] for d in json_data)
        except ValueError:
            last_updated = datetime.now().isoformat()

        last_updated = datetime.fromisoformat(last_updated)
        last_updated = int(last_updated.timestamp())

        path = f'./topics/{topic}/{topic}.json'

        with open(path, 'r') as f:
            content = f.read()
            conf = json.loads(content)
            conf['from'] = last_updated

        with open(path, 'w') as file:
            json.dump(conf, file, indent=4)

    return json_data
