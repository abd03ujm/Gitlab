import yaml
import json
import sys

# Load YAML
with open('service.yaml') as f:
    data = yaml.safe_load(f)

# Correct path to contacts
#---------- Validate Contacts ----------
contacts = data.get("metadata", {}).get("contacts", [])

# Ensure it's a list
if not isinstance(contacts, list):
    print(" Error: 'metadata.contacts' field is missing or not a list.")
    sys.exit(1)

# Validation logic
allowed_contact_types = {"email", "slack", "link", "slack", "microsoft-teams"}
invalid_contacts = []

for contact in contacts:
    contact_type = str(contact.get("type", "")).strip().lower()
    if contact_type not in allowed_contact_types:
        invalid_contacts.append(contact)

# Output result
if invalid_contacts:
    print(" Invalid contact types found: Allowed contact types are: ", ', '.join(allowed_contact_types))
    

    sys.exit(1)
else:
    print(" All contact types are valid.")

#---------- Validate Links ----------
links = data.get("metadata", {}).get("links", [])
allowed_link_types = {"repo", "docs", "dashboard"}
allowed_repo_providers = {"github", "bitbucket", "gitlab"}
invalid_links = []

if not isinstance(links, list):
    print(" Error: 'metadata.links' field is missing or not a list.")
    sys.exit(1)

for link in links:
    link_type = str(link.get("type", "")).strip().lower()
    provider = str(link.get("provider", "")).strip().lower()

    # Check if the link type itself is valid
    if link_type not in allowed_link_types:
        invalid_links.append({
            "name": link.get("name"),
            "error": f"Invalid link type '{link_type}'"
        })

    # Check repo providers only if type is repo
    elif link_type == "repo" and provider not in allowed_repo_providers:
        invalid_links.append({
            "name": link.get("name"),
            "error": f"Invalid provider '{provider}' for type 'repo'"
        })
    
    
if invalid_links:
    print(
        "\n Invalid links found:\n" +
        "\n".join(f" - {il['name']}: {il['error']}" for il in invalid_links) +
        f"\n\n Allowed link types: {', '.join(allowed_link_types)}" +
        f"\n Allowed repo providers: {', '.join(allowed_repo_providers)}"
    )
    sys.exit(1)
else:
    print(" All links type and providers are valid.")

#---------- Validate Languages and Language type----------

spec = data.get("spec", {})
spec_type = str(spec.get("type", "")).strip().lower()
allowed_spec_types = {"web", "db", "cache", "function", "function", "browser", "mobile"}

if spec_type not in allowed_spec_types:
    print(f" Invalid spec.type: '{spec_type}'")
    print(f"   Allowed types are: {', '.join(allowed_spec_types)}")
    sys.exit(1)
else:
    print(f"spec language type is valid")

#------- Save to JSON -------
with open('service.json', 'w') as f:
    json.dump(data, f, indent=2)



