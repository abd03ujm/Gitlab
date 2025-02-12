#!/bin/bash
echo "Generating matrix.yml..."
echo "matrix:" > matrix.yml
echo "  - NODE_DIR: [" >> matrix.yml

while read -r line; do
    echo "      \"$line\"," >> matrix.yml
done < node_versions.txt

sed -i '$ s/,$//' matrix.yml  # Remove last comma
echo "    ]" >> matrix.yml
