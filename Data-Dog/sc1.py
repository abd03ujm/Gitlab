import json
import ast  # for safely parsing list values from strings

def parse_value(value):
    try:
        return ast.literal_eval(value)  # safely convert string lists to real lists
    except:
        return value.strip()

# Read config file
data = {}
with open("service_info_1.txt", "r") as file:
    for line in file:
        if "=" in line:
            key, value = line.strip().split("=", 1)
            data[key.strip()] = parse_value(value.strip())

# Build final JSON structure
final_json = {
    "apiVersion": "v3",
    "kind": "service",
    "metadata": {
        "name": data.get("name"),
        "description": data.get("description"),
        "displayName": data.get("displayName"),
        "tags": data.get("tag", []),
        "owner": data.get("owner"),
        "links": [
            {
                "name": name,
                "type": type_,
                "provider": provider,
                "url": url
            }
            for name, type_, provider, url in zip(
                data.get("link_name", []),
                data.get("link_type", []),
                data.get("link_provider", []),
                data.get("link_url", [])
            )
        ],
        "contacts": [
            {
                "name": name,
                "type": type_,
                "contact": email
            }
            for name, type_, email in zip(
                data.get("contact_name", []),
                data.get("contact_type", []),
                data.get("contact_email", [])
            )
        ],
        "additionalOwners": [
            {
                "name": name,
                "type": type_
            }
            for name, type_ in zip(
                data.get("additional_owner_name", []),
                data.get("additional_owner_type", [])
            )
        ]
    },
    "datadog": {
        "pipelines": {
            "fingerprints": data.get("pipeline_fingerprint", [])
        }
    },
    "spec": {
        "lifecycle": data.get("lifecycle"),
        "tier": data.get("tier"),
        "languages": data.get("language", []),
        "type": data.get("type"),
        "dependsOn": data.get("dependsOn", []),
        "componentOf": data.get("componentOf", [])
    }
}

# Output JSON
print(json.dumps(final_json, indent=2))
