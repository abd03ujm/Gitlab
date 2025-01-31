```bash
kubectl create secret docker-registry my-docker-secret \
  --docker-server=<REGISTRY_URL> \
  --docker-username=<DOCKER_USERNAME> \
  --docker-password=<DOCKER_PASSWORD> \
  --docker-email=<DOCKER_EMAIL>
```
jobs:build config contains unknown keys: volumes, volumesmounts
