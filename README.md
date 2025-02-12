```bash
kubectl create secret docker-registry my-docker-secret \
  --docker-server=<REGISTRY_URL> \
  --docker-username=<DOCKER_USERNAME> \
  --docker-password=<DOCKER_PASSWORD> \
  --docker-email=<DOCKER_EMAIL>
```
jobs:build config contains unknown keys: volumes, volumesmounts
INFO[0022] Pushing image to docker.hyattdev.com/docker/alpine-node:node-18.20.6-alpine3.20 
error pushing image: failed to push to destination docker.hyattdev.com/docker/alpine-node:node-18.20.6-alpine3.20: PUT https://docker.hyattdev.com/v2/docker/alpine-node/manifests/node-18.20.6-alpine3.20: MANIFEST_INVALID: manifest invalid; map[description:null]


$ /kaniko/executor --context "${CI_PROJECT_DIR}/${NODE_DIR}" --dockerfile "${CI_PROJECT_DIR}/${NODE_DIR}/Dockerfile" --destination "${FINAL_IMAGE}"
INFO[0000] Retrieving image manifest alpine:3.21.0      
INFO[0000] Retrieving image alpine:3.21.0 from registry index.docker.io 
INFO[0002] Built cross stage deps: map[]                
INFO[0002] Retrieving image manifest alpine:3.21.0      
INFO[0002] Returning cached image manifest              
INFO[0002] Executing 0 build triggers                   
WARN[0002] MAINTAINER is deprecated, skipping           
INFO[0002] Building stage 'alpine:3.21.0' [idx: '0', base-idx: '-1'] 
INFO[0002] Skipping unpacking as no commands require it. 
INFO[0002] WORKDIR $appDir                              
INFO[0002] Cmd: workdir                                 
INFO[0002] Changed working directory to /               
INFO[0002] No files changed in this command, skipping snapshotting. 
INFO[0002] Pushing image to docker.hyattdev.com/docker/gitlab-poc:alpine3.21.0 
error pushing image: failed to push to destination docker.hyattdev.com/docker/gitlab-poc:alpine3.21.0: PUT https://docker.hyattdev.com/v2/docker/gitlab-poc/manifests/alpine3.21.0: MANIFEST_INVALID: manifest invalid; map[description:null]
Cleaning up project directory and file based variables
00:00
ERROR: Job failed: command terminated with exit code 1
