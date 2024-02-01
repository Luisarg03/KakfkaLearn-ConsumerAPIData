import requests
import json
from datetime import datetime

# URL de la API
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
    selected_attributes = {}
    for attribute in attributes:
        if attribute in d:
            selected_attributes[attribute] = d[attribute]
        else:
            selected_attributes[attribute] = None
    selected_attributes['timestamp'] = datetime.now().isoformat()
    data_filter.append(selected_attributes)

print(data_filter)