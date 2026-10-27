
pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                sh 'docker build -t gokul141006/task-manager:v2 .'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_PASS'
                    )
                ]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login \
                          -u "$DOCKER_USER" --password-stdin
                        docker push gokul141006/task-manager:v2
                        docker logout
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([
                    string(
                        credentialsId: 'k8s-token',
                        variable: 'K8S_TOKEN'
                    )
                ]) {
                    sh '''
                        kubectl \
                          --server=https://host.docker.internal:52844 \
                          --token="$K8S_TOKEN" \
                          --insecure-skip-tls-verify=true \
                          apply -f k8s/deployment-v2.yaml

                        kubectl \
                          --server=https://host.docker.internal:52844 \
                          --token="$K8S_TOKEN" \
                          --insecure-skip-tls-verify=true \
                          apply -f k8s/service-v2.yaml

                        kubectl \
                          --server=https://host.docker.internal:52844 \
                          --token="$K8S_TOKEN" \
                          --insecure-skip-tls-verify=true \
                          rollout status deployment/task-manager-v2
                    '''
                }
            }
        }
    }
}
