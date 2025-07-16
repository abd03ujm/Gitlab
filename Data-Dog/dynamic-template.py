# import yaml
# import json
# import sys

# with open('dd-sc-info.yaml') as f:
#     data = yaml.safe_load(f)

# with open('service.json', 'w') as f:
#     json.dump(data, f, indent=2)

import yaml
import json
import sys

# Define symbols
correct_symbol = "✅"
wrong_symbol = "❌"

# Load YAML
try:
    with open('service-info.yaml') as f:
        data = yaml.safe_load(f)
except Exception as e:
    print(f"{wrong_symbol} Failed to load YAML: {e}")
    sys.exit(1)

#---------- Change metadata keys names----------
metadata = data.get("metadata", {})

field_renames = {
    "service_name": "name",
    "service_description": "description",
    "service_displayName": "displayName"
}

for old_key, new_key in field_renames.items():
    if old_key in metadata:
        metadata[new_key] = metadata.pop(old_key)

data["metadata"] = metadata
print(f"{correct_symbol} Renamed metadata fields: {', '.join(field_renames.values())}")


#---------- Change links keys names----------
link_field_renames = {
    "link_name": "name",
    "link_type": "type",
    "link_provider": "provider",
    "link_url": "url"
}

metadata_links = metadata.get("links", [])
if isinstance(metadata_links, list):
    for link in metadata_links:
        for old_key, new_key in link_field_renames.items():
            if old_key in link:
                link[new_key] = link.pop(old_key)

# ---------- Rename root-level links ----------
root_links = data.get("links", [])
if isinstance(root_links, list):
    for link in root_links:
        for old_key, new_key in link_field_renames.items():
            if old_key in link:
                link[new_key] = link.pop(old_key)

# Save updated metadata
data["metadata"] = metadata



# ---------- Validate Contacts ----------
contacts = data.get("metadata", {}).get("contacts", [])

if not isinstance(contacts, list):
    print(f"{wrong_symbol} Error: 'metadata.contacts' field is missing or not a list.")
    sys.exit(1)

allowed_contact_types = {"email", "slack", "link", "microsoft-teams"}
invalid_contacts = []

for contact in contacts:
    contact_type = str(contact.get("type", "")).strip().lower()
    if contact_type not in allowed_contact_types:
        invalid_contacts.append(contact)

if invalid_contacts:
    print(f"{wrong_symbol} Invalid contact types found!")
    print(f"   Allowed contact types: {', '.join(allowed_contact_types)}")
    for contact in invalid_contacts:
        print(f"   - Invalid type: {contact.get('type')}")
    sys.exit(1)
else:
    print(f"{correct_symbol} All contact types are valid.")

# ---------- Validate Links ----------
links = data.get("metadata", {}).get("links", [])
allowed_link_types = {"repo", "doc", "dashboard"}
allowed_repo_providers = {"github", "bitbucket", "gitlab"}
invalid_links = []

if not isinstance(links, list):
    print(f"{wrong_symbol} Error: 'metadata.links' field is missing or not a list.")
    sys.exit(1)

for link in links:
    link_type = str(link.get("type", "")).strip().lower()
    provider = str(link.get("provider", "")).strip().lower()

    if link_type not in allowed_link_types:
        invalid_links.append({
            "name": link.get("name"),
            "error": f"Invalid link type '{link_type}'"
        })
    elif link_type == "repo" and provider not in allowed_repo_providers:
        invalid_links.append({
            "name": link.get("name"),
            "error": f"Invalid provider '{provider}' for type 'repo'"
        })

if invalid_links:
    print(f"{wrong_symbol} Invalid links found:")
    for il in invalid_links:
        print(f"   - {il['name']}: {il['error']}")
    print(f"\n   Allowed link types: {', '.join(allowed_link_types)}")
    print(f"   Allowed repo providers: {', '.join(allowed_repo_providers)}")
    sys.exit(1)
else:
    print(f"{correct_symbol} All link types and providers are valid.")

# ---------- Validate Languages and Language type ----------
spec = data.get("spec", {})
spec_type = str(spec.get("type", "")).strip().lower()
allowed_spec_types = {"web", "db", "cache", "function", "browser", "mobile"}

if spec_type not in allowed_spec_types:
    print(f"{wrong_symbol} Invalid spec.type: '{spec_type}'")
    print(f"   Allowed types are: {', '.join(allowed_spec_types)}")
    sys.exit(1)
else:
    print(f"{correct_symbol} spec.type is valid.")

## ---------- Save to JSON ----------
try:
    with open('service-info.json', 'w') as f:
        json.dump(data, f, indent=2)
    print(f"{correct_symbol} Successfully saved data to service.json")
except Exception as e:
    print(f"{wrong_symbol} Failed to write JSON: {e}")
    sys.exit(1)
