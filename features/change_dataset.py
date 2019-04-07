import json
import os

CWD = os.getcwd()
JSON_CONFIG_FILE_PATH = '%s/%s' % (CWD, 'twitter-out2019-04-06T12_10_16.106Z.jsonl')
CONFIG_PROPERTIES = {}
with open(JSON_CONFIG_FILE_PATH, 'r', encoding="utf8") as f:
    data = [json.loads(line) for line in f]

print(data[0])

for i in range(0, len(data)):
    if (data[i]['postMedia']):
        first = data[i]['postMedia'][0]
        data[i]['id'] = first.split('.')[0]

print(data[8]['id'])
print(data[8]['postMedia'])

print(len(data))

for i in range(0, len(data)):
    with open('instances_modified.jsonl', 'a') as outfile:
        json.dump(data[i], outfile)
        outfile.write('\n')
