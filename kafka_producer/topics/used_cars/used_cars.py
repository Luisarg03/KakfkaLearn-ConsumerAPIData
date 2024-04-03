import json
from common.helpclass import CommonClass, CommonKakfa

with open('used_cars.json', 'r') as f:
    conf = json.load(f)
f.close()

kafka_instance = CommonKakfa(conf)
request_data = CommonClass(conf)
data = request_data.get_data()
data = data['results']
select_keys = conf['attr']['COLS']

data = [{k: v for k, v in d.items() if k in select_keys} for d in data]

for i in data:
    i = json.dumps(i)
    kafka_instance.kafka_produce(data=i)
