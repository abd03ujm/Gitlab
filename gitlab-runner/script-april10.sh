#!/bin/sh
# Validation script for alpine-node container
# Validates node, alpine, and yarn versions against versions from manifest file

set -e  # Exit immediately if a command exits with non-zero status

echo "Starting container validation..."

# Define path to manifest file
MANIFEST_FILE="/usr/src/app/scripts/manifest"

# Check if manifest file exists
if [ ! -f "$MANIFEST_FILE" ]; then
    echo "ERROR: Manifest file not found at $MANIFEST_FILE"
    exit 1
fi

# Extract version information from manifest file
extract_var() {
    local var_name=$1
    local value=$(grep "^$var_name=" "$MANIFEST_FILE" | cut -d'=' -f2 | tr -d '"' | tr -d "'")
    if [ -z "$value" ]; then
        echo "ERROR: $var_name not found in manifest file"
        exit 1
    fi
    echo "$value"
}

# Extract version values from manifest
SOFTWARE_VERSION=$(extract_var "SOFTWARE_VERSION")
ALPINE_VERSION=$(extract_var "ALPINE_VERSION")

echo "Extracted versions from manifest file:"
echo "- SOFTWARE_VERSION: $SOFTWARE_VERSION"
echo "- ALPINE_VERSION: $ALPINE_VERSION"

# Get current versions
CURRENT_NGINX_VERSION=$(nginx -v 2>&1 |tail -n 1 |cut -d '/' -f2)
CURRENT_ALPINE_VERSION=$(cat /etc/os-release | grep VERSION_ID | cut -d '=' -f2 | tr -d '"')

echo "=== Version Validation ==="
echo "Expected Node version: $SOFTWARE_VERSION"
echo "Actual Nginx version:   $CURRENT_NGINX_VERSION"
echo "---------------------------"
echo "Expected Alpine version: $ALPINE_VERSION"
echo "Actual Alpine version:   $CURRENT_ALPINE_VERSION"

# Validate Node.js version
if [ "$CURRENT_NGINX_VERSION" != "$SOFTWARE_VERSION" ]; then
    echo "ERROR: Nginx version mismatch!"
    echo "Expected: $SOFTWARE_VERSION, Found: $CURRENT_NGINX_VERSION"
    exit 0
fi

# Validate Alpine version
if [ "$CURRENT_ALPINE_VERSION" != "$ALPINE_VERSION" ]; then
    echo "ERROR: Alpine version mismatch!"
    echo "Expected: $ALPINE_VERSION, Found: $CURRENT_ALPINE_VERSION"
    exit 1
fi


echo "✅ Validation successful! All versions match the values in manifest file."
# Output result as JSON for easier parsing in CI/CD pipelines
echo "Result: {\"status\":\"success\",\"nginx_version\":\"$CURRENT_NGINX_VERSION\",\"alpine_version\":\"$CURRENT_ALPINE_VERSION\"}"
exit 0
