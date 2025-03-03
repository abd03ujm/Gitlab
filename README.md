```bash
kubectl create secret docker-registry my-docker-secret \
  --docker-server=<REGISTRY_URL> \
  --docker-username=<DOCKER_USERNAME> \
  --docker-password=<DOCKER_PASSWORD> \
  --docker-email=<DOCKER_EMAIL>


```
1. ```How we will do```   --> Install Docker daemon on Kubernetes cluster  - Need root access to install docker

2  ```What issues will be resolved``` --> Eliminate the Dockerdind(Running Docker inside Docker adds an extra layer of abstraction, leading to increased CPU and memory consumption. / The nested environment may cause disk I/O bottlenecks.)

3. ```After that do we need dnd image```  -->  No 

5. ```What if any issues we can expect``` - -> No issues ( To test workflow and issues  - Recomond  to install on one worker node and label the node to use it in gitlab-runner-test)

6. ```Blackout plan```  --> Revert back the changes
