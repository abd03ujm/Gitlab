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




```yaml
gitlabUrl: "http://192.168.1.120"
runnerRegistrationToken: "glrt-7X6ynXvvkZz6oPkbpPXQ"
serviceAccountName: "gitlab-runner-sa"
runnerTags: "k8s-runner"
rbac:
  create: true
runners:
  config: |
    [[runners]]
      name = "k8-docker-runner"
      url = "http://192.168.1.120/"
      token = "glrt-Fsk9WJQ12LsbByB7nAg_"
      executor = "kubernetes"
      [runners.kubernetes]
        image = "docker:25.0.3"
        privileged = true
        [runners.kubernetes.volumes]
          [[runners.kubernetes.volumes.host_path]]
            name = "docker-socket"
            mount_path = "/var/run/docker.sock"
            host_path = "/var/run/docker.sock"
        # Corrected node_selector syntax
        [runners.kubernetes.node_selector]
          "gitlab-runner" = "true"


```

```bash
curl https://releases.rancher.com/install-docker/25.0.5.sh | sh

systemctl enable docker

systemctl start docker

```



# Get Java version 
```bash
java -version 2>&1 | grep -oP '(?<=version ")([^"]+)'
```
