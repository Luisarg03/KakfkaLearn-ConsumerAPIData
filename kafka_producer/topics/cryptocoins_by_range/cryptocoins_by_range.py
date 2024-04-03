import json
import pandas as pd
from common.helpclass import CommonClass, CommonKakfa

with open('cryptocoins_by_range.json', 'r') as f:
    conf = json.load(f)
f.close()

kafka_instance = CommonKakfa(conf)
request_data = CommonClass(conf)
data = request_data.get_data()

data = pd.DataFrame(data)
data['date_unix'] = data['prices'].apply(lambda x: x[0])
data['prices'] = data['prices'].apply(lambda x: x[1])
data['market_caps'] = data['market_caps'].apply(lambda x: x[1])
data['total_volumes'] = data['total_volumes'].apply(lambda x: x[1])

for i in range(len(data)):
    kafka_instance.kafka_produce(data=data.iloc[i].to_json())
