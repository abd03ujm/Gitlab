package com.hyatt.ci.platform

// Hyatt Confidential
// by Robert Stevenson

private def found_existing_image(repo) {
  if (env.GIT_TAG_MATCH == null || env.GIT_TAG_MATCH == "null") {
    return false
  }
  if (repo == env.GIT_TAG_MATCH_REPO) {
    return true
  }
  return false
}

def is_pr(change_id) {
  if (change_id == null || change_id == 'null') {
    return false
  }
  return true
}

def copy_image(artifactory_location, projectname, sourceRepo, sourceTag, targetRepo, targetTag) {
  // promote image to production repository (file-move), removing the original dockerv2-local version
  def body = "{\"targetRepo\" : \"${targetRepo}\", " +
          "\"dockerRepository\" : \"${artifactory_location.toLowerCase()}/${projectname}\", " +
          "\"tag\" : \"${sourceTag}\", " +
          "\"targetTag\" : \"${targetTag}\", " +
          "\"copy\": \"true\"} "

  echo "Copying docker image [${artifactory_location.toLowerCase()}/${projectname}:${sourceTag}] to ${targetRepo} repo"
  def result
  withCredentials([string(credentialsId: 'jenkins_upload_api_key', variable: 'KEY')]) {
    result = httpRequest url: "https://artifacts.hyattdev.com/artifactory/api/docker/${sourceRepo}/v2/promote",
            httpMode: "POST",
            contentType: "APPLICATION_JSON",
            requestBody: body,
            customHeaders: [[name: 'X-JFrog-Art-Api', value: KEY]],
            validResponseCodes: "200,404"
  }
}

def promote_image(artifactory_location, projectname, sourceTag, skipProdRepoCheck) {
 promote_tagged_image(artifactory_location, projectname, "dockerv2-local", sourceTag, sourceTag.replace(".beta",""), skipProdRepoCheck, false) 
}

def promote_tagged_image(artifactory_location, projectname, sourceRepo, sourceTag, targetTag, skipProdRepoCheck, doCopy) {
  //  Artifactory.docker.promote promotionConfig 

  // promote image to production repository (file-move), removing the original dockerv2-local version
  def body = "{\"targetRepo\" : \"dockerv2-prod\", " +
          "\"dockerRepository\" : \"${artifactory_location.toLowerCase()}/${projectname}\", " +
          "\"tag\" : \"${sourceTag}\", " +
          "\"targetTag\" : \"${targetTag}\", " +
          "\"copy\": \"${doCopy}\"} "

  if (!is_pr(env.CHANGE_ID)) {
    if (!found_existing_image("dockerv2-prod")) {

      if (find_docker_image_with_tag("${projectname}", "${sourceRepo}", "${sourceTag}")) {
        echo "found image in ${sourceRepo} ${projectname}:${sourceTag}"
        if (skipProdRepoCheck == true || find_docker_image_with_tag("${projectname}", "dockerv2-prod", "${targetTag}") == null) {
          if ( !skipProdRepoCheck ) {
            echo "did not find image in dockerv2-prod ${artifactory_location.toLowerCase()}/${projectname}:${sourceTag}"
          } else {
            echo "skipping prod repo check"
          }

          echo "Promoting/moving docker image [${artifactory_location.toLowerCase()}/${projectname}:${sourceTag}] to ${targetTag} dockerv2-prod repo"
          def result
          withCredentials([string(credentialsId: 'jenkins_upload_api_key', variable: 'KEY')]) {
            result = httpRequest url: "https://artifacts.hyattdev.com/artifactory/api/docker/${sourceRepo}/v2/promote",
                    httpMode: "POST",
                    contentType: "APPLICATION_JSON",
                    requestBody: body,
                    customHeaders: [[name: 'X-JFrog-Art-Api', value: KEY]],
                    validResponseCodes: "200,404"
          }
        } else {
          echo "found image in dockerv2-prod ${artifactory_location.toLowerCase()}/${projectname}:${sourceTag} skipping promotion"
        }
      } else {
        echo "did not find image in ${sourceRepo} ${artifactory_location.toLowerCase()}/${projectname}:${sourceTag}, skipping promotion"
      }
    } else {
      echo "Not promoting due to artifactory image match"
    }
  } else {
    echo "Not promoting due to PR"
  }
}

def promote_pipeline_stable(artifactory_location, projectname) {
  //  Artifactory.docker.promote promotionConfig 

  // copy tagged image to pipeline-stable tag, retaining the original image tag
  def body = "{\"targetRepo\" : \"dockerv2-prod\", " +
          "\"dockerRepository\" : \"${artifactory_location}/${projectname}\", " +
          "\"tag\" : \"${env.DOCKER_TAG}\", " +
          "\"targetTag\" : \"pipeline-stable\", " +
          "\"copy\": true} "

  if (!is_pr(env.CHANGE_ID)) {
    if (!found_existing_image("dockerv2-prod")) {
      echo "Promoting docker image to dockerv2-prod :pipeline-stable tag "
      try {
        def result
        withCredentials([string(credentialsId: 'jenkins_upload_api_key', variable: 'KEY')]) {
          result = httpRequest url: "https://artifacts.hyattdev.com/artifactory/api/docker/dockerv2-prod/v2/promote",
                  httpMode: "POST",
                  contentType: "APPLICATION_JSON",
                  requestBody: body,
                  customHeaders: [[name: 'X-JFrog-Art-Api', value: KEY]],
                  validResponseCodes: "200,404"
        }
      }
      catch (err) {
        // ignore any promotion errors, because the old docker pipeline promotes already, so this one will fail
      }
    } else {
      echo "promote_pipeline_stable, found existing image"
    }
  } else {
    echo "promote_pipeline_stable, is a PR"
  }
}

/*
we actually need to look in local repo and prod repo for a matching image
 */

def find_docker_image(servicename, branch, equality) {
  find_docker_image0(servicename, branch, equality, "docker")
}

private def find_docker_image_with_tag(servicename, repo, tag) {

  def body = "items.find({\"repo\" : {\"\$eq\":\"${repo}\"}}," +
          "{\"path\":{\"\$match\":\"${env.artifactory_location}/${servicename}/${tag}\"}})" +
          ".sort({\"\$desc\":[\"created\"]})" +
          ".limit(1) "

  def result
  withCredentials([string(credentialsId: 'jenkins_upload_api_key', variable: 'KEY')]) {
    result = httpRequest url: "https://artifacts.hyattdev.com/artifactory/api/search/aql",
            contentType: "TEXT_PLAIN",
            httpMode: "POST",
            requestBody: body,
            customHeaders: [[name: 'X-JFrog-Art-Api', value: KEY]]
  }

  def object = readJSON text: result.content

  if (object != null && object.results != null && object.results[0] != null) {
    path = object.results[0].path
    // replace the last slash with a : for the tag
    int index = path.lastIndexOf("/")
    return path.substring(index + 1)
  } else {
    return null
  }
}

private def find_docker_image0(servicename, branch, equality, repo) {

  def body = "items.find({\"repo\" : {\"\$eq\":\"${repo}\"}}," +
          "{\"@docker.label.git.branch\" : {\"\$${equality}\" : \"${branch.replace("/", "-").replace(".", "-")}\"}}," +
          "{\"path\":{\"\$match\":\"${env.artifactory_location}/${servicename}/*\"}})" +
          ".sort({\"\$desc\":[\"created\"]})" +
          ".limit(1) "
  def result
  withCredentials([string(credentialsId: 'jenkins_upload_api_key', variable: 'KEY')]) {
    result = httpRequest url: "https://artifacts.hyattdev.com/artifactory/api/search/aql",
            contentType: "TEXT_PLAIN",
            httpMode: "POST",
            requestBody: body,
            customHeaders: [[name: 'X-JFrog-Art-Api', value: KEY]]
  }

  def object = readJSON text: result.content

  if (object != null && object.results != null && object.results[0] != null) {
    path = object.results[0].path
    // replace the last slash with a : for the tag
    int index = path.lastIndexOf("/")
    return path.substring(index + 1)
  } else {
    return null
  }
}

def find_docker_image_by_sum(servicename, sum, equality) {
  find_docker_image_by_sum0(servicename, sum, equality, "docker")
}

private def find_docker_image_by_sum0(servicename, sum, equality, repo) {

  def extension
  def projectName = servicename
  if (env["buildonly"]) {
    if (env.buildonly == true || env.buildonly == "true") {
      projectName = "${projectName}-buildonly"
    }
  }
  if (env["custombuild"]) {
    if (env.custombuild == true || env.custombuild == "true") {
      projectName = "${projectName}-buildonly"
    }
  }

  def body = "items.find({\"repo\" : {\"\$eq\":\"${repo}\"}}," +
          "{\"@docker.label.source.sum\" : {\"\$${equality}\" : \"${sum}\"}}," +
          "{\"path\":{\"\$match\":\"*${env.artifactory_location}/${projectName}/*\"}})" +
          ".sort({\"\$desc\":[\"created\"]})" +
          ".limit(1) "

  echo body

  def k
  def result
  withCredentials([string(credentialsId: 'jenkins_upload_api_key', variable: 'KEY')]) {
    k = "${KEY}"
    result = httpRequest url: "https://artifacts.hyattdev.com/artifactory/api/search/aql",
            contentType: "TEXT_PLAIN",
            httpMode: "POST",
            customHeaders: [[name: 'X-JFrog-Art-Api', value: KEY]],
            requestBody: body
  }
//  echo k

  def object = readJSON text: result.content

  echo object.toString()

  def repository
  if (object != null && object.results != null && object.results[0] != null) {
    path = object.results[0].path
    // replace the last slash with a : for the tag
    int index = path.lastIndexOf("/")
    repository = object.results[0].repo
    return [path.substring(index + 1), repository]
  } else {
    return [null,null]
  }
}

def find_docker_version_by_name(imagename) {

  def result
  withCredentials([string(credentialsId: 'jenkins_upload_api_key', variable: 'KEY')]) {
    result = httpRequest url: "https://artifacts.hyattdev.com/artifactory/api/storage/docker/docker/${imagename.replace(":", "/")}/manifest.json?properties",
            contentType: "TEXT_PLAIN",
            httpMode: "GET",
            customHeaders: [[name: 'X-JFrog-Art-Api', value: KEY]]

  }

  def object = readJSON text: result.content

  echo object.toString()

  if (object != null && object.properties != null) {
    properties = object.properties
    if (properties['docker.label.docker.tag'] != null) {
      return properties['docker.label.docker.tag'][0]
    }
  } else {
    return null
  }
}

def get_dependency_docker_image_tags(dep_list) {
  dep_versions = []
  def artifactory = new com.hyatt.ci.platform.Artifactory()
  for (dep in dep_list) {
    // if current branch version is out there grab its version
    docker_tag = artifactory.find_docker_image(dep, git_branch_to_build, "eq")
    if (docker_tag == null) {
      // if master branch version is out there grab its version
      docker_tag = artifactory.find_docker_image(dep, "master", "eq")
      if (docker_tag == null) {
        // else just grab latest built version
        docker_tag = artifactory.find_docker_image(dep, "", "ne")
      }
    }
    if (docker_tag == null) {
      //dep_versions.push("${dep}-deployed-image-not-found")
      //fail "${dep} docker image missing..."
      //dep_versions.push(env.DOCKER_TAG)
      return dep_versions
    } else {
      dep_versions.push(docker_tag)
    }
  }
  return dep_versions
}
