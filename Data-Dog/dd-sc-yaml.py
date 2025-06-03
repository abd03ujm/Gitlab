import yaml
import json
import sys

with open('service.yaml') as f:
    data = yaml.safe_load(f)

with open('service.json', 'w') as f:
    json.dump(data, f, indent=2)
