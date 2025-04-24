#!/bin/sh

echo "==== Starting Java App ===="
echo "OS Info:"
cat /etc/os-release || echo "No OS info found"

echo "Java Version:"
java -version 2>&1

# (Optional) Add other middleware versions here
# e.g., tomcat version, mysql --version, etc.

echo "==========================="
echo "Launching App..."
exec java App
