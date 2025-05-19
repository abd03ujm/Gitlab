import json
from datetime import datetime

# Read text file
data = {}
with open("service_info.txt", "r") as file:
    for line in file:
        if "=" in line:
            key, value = line.strip().split("=", 1)
            data[key] = value

# Build final JSON structure
final_json = {
    "apiVersion": "v3",
    "kind": "service",
    "metadata": {
        "name": data.get("name"),
        "description": data.get("description"),
        "displayName": data.get("displayName"),
        "tags": [
            data.get("tag")
        ],
        "owner": data.get("owner"),
        "links": [
            {
                "name": data.get("link_name"),
                "type": data.get("link_type"),
                "provider": data.get("link_provider"),
                "url": data.get("link_url")
            }
        ],
        "contacts": [
            {
                "name": data.get("contact_name"),
                "type": data.get("contact_type"),
                "contact": data.get("contact_email")
            }
        ],
        "additionalOwners": [
            {
                "name": data.get("additional_owner_name"),
                "type": data.get("additional_owner_type")
            }
        ]
    },
    "datadog": {
        "pipelines": {
            "fingerprints": [
                data.get("pipeline_fingerprint")
            ]
        }
    },
    "spec": {
        "lifecycle": data.get("lifecycle"),
        "tier": data.get("tier"),
        "languages": [
            data.get("language")
        ],
        "type": data.get("type"),
        "dependsOn": [
            data.get("dependsOn")
        ],
        "componentOf": [
            data.get("componentOf")
        ]
    }
}

# Output the final JSON
print(json.dumps(final_json, indent=2))
