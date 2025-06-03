import yaml
import json
import requests

# Replace these with your actual API and APP keys
DD_API_KEY = "your_api_key_here"
DD_APP_KEY = "your_app_key_here"

# Load YAML file
with open("service.yaml", "r") as f:
    yaml_data = yaml.safe_load(f)

# Datadog API endpoint for Software Catalog services
url = "https://api.datadoghq.com/api/v2/software-catalog/services"

headers = {
    "Content-Type": "application/json",
    "DD-API-KEY": DD_API_KEY,
    "DD-APPLICATION-KEY": DD_APP_KEY,
}

# Convert YAML to JSON string
payload = json.dumps(yaml_data)

# POST request to create or update service
response = requests.post(url, headers=headers, data=payload)

if response.status_code in (200, 201):
    print("Service catalog updated successfully!")
else:
    print(f"Failed to update: {response.status_code} - {response.text}")
