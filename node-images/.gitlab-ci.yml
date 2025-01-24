stages:
  - build

variables:
  IMAGE_NAME: registry.example.com/your-project/node-alpine

build_images:
  stage: build
  image: docker:stable
  services:
    - docker:dind
  # variables:
  #   DOCKER_TLS_CERTDIR: "/certs"
  parallel: 
    matrix:
      - NODE_VERSION: ["20", "18", "22"]
  script:
    - echo $NODE_VERSION

    - echo docker build --build-arg NODE_VERSION=$NODE_VERSION -t $IMAGE_NAME:$NODE_VERSION -f Dockerfile
    - echo push $IMAGE_NAME:$NODE_VERSION
  only:
    - main
  tags:
    - k8s-runner
##
