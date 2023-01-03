pipeline {
    agent {
      kubernetes  {
            label 'jenkins-slave'
             defaultContainer 'jnlp'
      yaml """
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: dind
    image: docker:18.09-dind
    securityContext:
      privileged: true
  - name: docker
    env:
    - name: DOCKER_HOST
      value: jenkins-ag:2375
    image: docker:18.09
    command:
    - cat
    tty: true
  - name: tools
    image: argoproj/argo-cd-ci-builder:v1.0.0
    command:
    - cat
    tty: true
"""
        }
    }
  environment {
      IMAGE_REPO = "registry.iab.ai/rsvp"
      REGISTRY = "registry.iab.ai"
      // Instead of DOCKERHUB_USER, use your Dockerhub name
  }
  stages {
    stage('Build') {
      environment {
        DOCKERHUB_CREDS = credentials('registryiabai')
      }
      steps {
        container('docker') {
          sh "echo ${env.GIT_COMMIT}"
          // Build new image
          sh "until docker container ls; do sleep 3; done && docker image build -t  ${env.IMAGE_REPO}:${env.GIT_COMMIT} ."
          // Publish new image
          sh "docker login $REGISTRY --username $DOCKERHUB_CREDS_USR --password $DOCKERHUB_CREDS_PSW && docker image push ${env.IMAGE_REPO}:${env.GIT_COMMIT}"
        }
      }
    }
    stage('Deploy') {
      environment {
        GIT_CREDS = credentials('b009a837-3a84-4d48-811f-5bde4bddf969')
        HELM_GIT_REPO_URL = "github.com/ansenio/rsvpapp-helm-cicd.git"
        GIT_REPO_EMAIL = 'andrea.sannuto@gmx.com'
        GIT_REPO_BRANCH = "master"
        ARGOCD_CREDS = credentials('argocdiabai')
        ARGOCD_SERVER = 'argo.iab.ai'
       // Update above variables with your user details
      }
      steps {
        container('tools') {
            sh "git clone https://${env.HELM_GIT_REPO_URL}"
            sh "git config --global user.email ${env.GIT_REPO_EMAIL}"
             // install wq
//             sh "wget https://github.com/mikefarah/yq/releases/download/v4.9.6/yq_linux_amd64.tar.gz"
//  downloading latest YQ https://github.com/mikefarah/yq/tree/master
            sh "wget -q https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64"
//             sh "tar xvf yq_linux_amd64.tar.gz"
            sh "chmod +x yq_linux_amd64"
            sh "mv yq_linux_amd64 /usr/bin/yq"
            sh "git checkout -b master"
          dir("rsvpapp-helm-cicd") {
              sh "git checkout ${env.GIT_REPO_BRANCH}"
            //install done
            sh '''#!/bin/bash
              echo $GIT_REPO_EMAIL
              echo $GIT_COMMIT
              ls -lth
              yq eval '.image.repository = env(IMAGE_REPO)' -i values.yaml
              yq eval '.image.tag = env(GIT_COMMIT)' -i values.yaml
              cat values.yaml
              pwd
              git add values.yaml
              echo 'a $GIT_COMMIT b env(GIT_COMMIT) c ${env.GIT_COMMIT}'

              git commit -m 'Triggered Build $GIT_COMMIT'
              git push https://$GIT_CREDS_USR:$GIT_CREDS_PSW@github.com/$GIT_CREDS_USR/rsvpapp-helm-cicd.git
            '''
          }
          sh 'wget -q https://github.com/argoproj/argo-cd/releases/download/v2.4.2/argocd-linux-amd64'
          sh 'mv argocd-linux-amd64 argocd'
          sh 'chmod +x argocd'
          sh 'mv argocd /usr/local/bin'
          sh 'echo logging to $ARGOCD_SERVER as $ARGOCD_CREDS_USR '
          sh 'argocd login  $ARGOCD_SERVER --username $ARGOCD_CREDS_USR --password $ARGOCD_CREDS_PSW --grpc-web '
          sh 'argocd app sync rpsvpapp'
          sh 'argocd version'
          sh 'argocd app get rpsvpapp --output json | yq -r ".status.sync.status"'
        }
      }
    }
  }
}