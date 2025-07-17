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

#---------- Replace key names----------
metadata = data.get("metadata", {})

field_renames = {
    "service_name": "name",
    "service_description": "description",
    "service_displayName": "displayName",
    "service_tags": "tags",
    "service_owner": "owners",
}

link_field_renames = {
    "service_link_name": "name",
    "service_link_type": "type",
    "service_link_provider": "provider",
    "service_link_url": "url"
}

contact_field_renames = {
    "service_contact_name": "name",
    "service_contact_type": "type",
    "service_contact_contact": "contact"
}
additional_owners_field_renames = {
    "service_additionalOwner_name": "name",
    "service_additionalOwner_type": "type",
}
datadog_fields_renames = {
    "service_pipelines": "pipelines",
}
datadog_fields_renames_fingerprint = {
    "service_fingerprints": "fingerprints"
}

spec_renames = {
    "service_lifecycle": "lifecycle",
    "service_tier": "tier",
    "service_languages": "languages",
    "service_type": "type",
    "service_dependsOn": "dependsOn",
    "service_componentOf": "componentOf"
   
}

#######################################################
for old_key, new_key in field_renames.items():
    if old_key in metadata:
        metadata[new_key] = metadata.pop(old_key)

data["metadata"] = metadata
print(f"{correct_symbol} Renamed metadata fields: {', '.join(field_renames.values())}")


#---------- Change links keys names----------


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

#------ Contact fields renaming----------

metadata_contacts = metadata.get("contacts", [])
if isinstance(metadata_contacts, list):
    for contact in metadata_contacts:
        for old_key, new_key in contact_field_renames.items():
            if old_key in contact:
                contact[new_key] = contact.pop(old_key)
#------------ Rename root-level contacts ----------
root_contacts = data.get("contacts", [])
if isinstance(root_contacts, list):
    for contact in root_contacts:
        for old_key, new_key in contact_field_renames.items():
            if old_key in contact:
                contact[new_key] = contact.pop(old_key)
# Save updated metadata contacts
data["metadata"] = metadata

#---- addtional owners renaming----------

additional_owners = metadata.get("additionalOwners", [])
if isinstance(additional_owners, list):
    for owner in additional_owners:
        for old_key, new_key in additional_owners_field_renames.items():
            if old_key in owner:
                owner[new_key] = owner.pop(old_key)
#------------ Rename root-level additional owners ----------
root_additional_owners = data.get("additionalOwners", [])
if isinstance(root_additional_owners, list):
    for owner in root_additional_owners:
        for old_key, new_key in additional_owners_field_renames.items():
            if old_key in owner:
                owner[new_key] = owner.pop(old_key)
# Save updated additional owners
data["metadata"] = metadata

#------------ Validate datadog  ----------

datadog = data.get("datadog", {})
for old_key, new_key in datadog_fields_renames.items():
    if old_key in datadog:
        datadog[new_key] = datadog.pop(old_key)

#-- root-level datadog fields renaming ----------
root_datadog = data.get("datadog", {})
for old_key, new_key in datadog_fields_renames.items():
    if old_key in root_datadog:
        root_datadog[new_key] = root_datadog.pop(old_key)
# Save updated datadog
data["datadog"] = datadog

#---------- Rename fingerprint field ----------

pipelines = data.get("datagog", {}).get("pipelines", [])
for old_key, new_key in datadog_fields_renames_fingerprint.items():
    if old_key in datadog:
        pipelines[new_key] = pipelines.pop(old_key)
data["datadog"] = datadog


#-- rot-level fingerprint renaming ----------
root_pipelines = data.get("datadog", {}).get("pipelines", [])
for old_key, new_key in datadog_fields_renames_fingerprint.items():
    if old_key in root_pipelines:
        root_pipelines[new_key] = root_pipelines.pop(old_key)

#- spec renaming ----------
spec = data.get("spec", {})

for old_key, new_key in spec_renames.items():
    if old_key in spec:
        spec[new_key] = spec.pop(old_key)
## root-level spec renaming
root_spec = data.get("spec", {})
for old_key, new_key in spec_renames.items():
    if old_key in root_spec:
        root_spec[new_key] = root_spec.pop(old_key)
data["spec"] = spec
#####################################################################################################
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
