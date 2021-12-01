import json

with open('data.txt', encoding='UTF-8') as json_file:
    data = json.load(json_file)
    for p in data['images']:
        print(p)