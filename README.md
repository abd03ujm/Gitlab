49
Copying blob sha256:a2a531a2f81e30102b8590328ef6699868b179bb6597611c373489745365fd4d
50
Copying blob sha256:bd9ddc54bea929a22b334e73e026d4136e5b73f5cc29942896c72e4ece69b13d
51
Copying config sha256:1277a65bdddb9a7ba850aef40842ff5eb62c83b697d73354058604e115c23961
52
Writing manifest to image destination
53
1277a65bdddb9a7ba850aef40842ff5eb62c83b697d73354058604e115c23961
54
reg-gitlab.hyattdev.com:5556/hyatt/digital-product/docker-images/alpine-java:1.8.0_442-54a9e544 
55
Error: normalizing name "": normalizing name "": repository name must have at least one component



************START ************
Q1 - As for now, if I have a non-default branch, with changes – will that also trigger the pipeline and publish the images to docker registry?
I think in common practice, we may want to lockdown the publishing to only default branch or “protected branch”?
If we go with this model, we’d ask all changes submitted via MR to default branch(or protected branch? Maybe we don’t need this for docker pipelines).
 
Q2 - Also, the current image build and image publish are both in the build job. Do we plan to separate them? Or can we separate them into two stages? For item 1, if I submit a change – will that trigger a “branch pipeline” just do the build to make sure the updated repo is buildable?
 
Q3 - I am not very sure how the “publish permission” got set – seems currently we are using your personal account? I long term, will that be extracted as”docker registry user” and “docker registry password”, and set in the group level(like digital product or even Hyatt?)
 
Q4 - ARTIFACTORY_URL and IMAGE_PATH are over lapping.
I think our target may be on artifactory but it might be any docker registry? So maybe name as something like “docker registry url” is better?
From the documentation, the sections are named as
[HOST[:PORT]/]NAMESPACE/REPOSITORY[:TAG]
So, the “host:port” is docker registry,
  Namespace/repository, maybe we can put thgether as “docker_repository”?
  Then tag is the part after “:”?
This is not big problem – just my 2 cents.

*****************END*************






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


GIT Repo Migration steps
1- create new project and clone it. for exmample repo name is: new-repo
2- in old-rep, run these commands:
   1- rm -rf .git
   2- cp -r * new-repo/     (* old-rep path     and mew-rep is new-repo path
   
