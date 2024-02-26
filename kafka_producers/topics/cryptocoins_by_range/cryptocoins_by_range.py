import uuid
import json
import requests
from datetime import datetime


def cryptocoins_by_range(conf: dict) -> list:
    # # REQUEST #
    url = conf['url']

    replacements = {
        '{{{COIN}}}': conf['attr']['COIN'],
        '{{{CURRENCY}}}': conf['attr']['CURRENCY'],
        '{{{from}}}': conf['from'],
        '{{{to}}}': conf['to']
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

    with open('./cryptocoins_by_range.json', 'r') as f:  # Cambia 'w' a 'r' para leer
        conf = json.load(f)  # Usa json.load para cargar el contenido JSON

    print(conf)

    return json_data
