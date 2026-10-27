<<<<<<< Updated upstream
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
                sh 'docker build -t gokul141006/task-manager:v1 .'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-creds',
                    usernameVariable: 'DOCKER_USER',
                    passwordVariable: 'DOCKER_TOKEN'
                )]) {
                    sh '''
                        set +x
                        echo "$DOCKER_TOKEN" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push gokul141006/task-manager:v1
                        docker logout
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withCredentials([string(
                    credentialsId: 'k8s-token',
                    variable: 'K8S_TOKEN'
                )]) {
                    sh '''
                        set +x

                        kubectl \
                          --server=https://host.docker.internal:52844 \
                          --token="$K8S_TOKEN" \
                          --insecure-skip-tls-verify=true \
                          apply -f k8s/deployment.yaml

                        kubectl \
                          --server=https://host.docker.internal:52844 \
                          --token="$K8S_TOKEN" \
                          --insecure-skip-tls-verify=true \
                          apply -f k8s/service.yaml

                        kubectl \
                          --server=https://host.docker.internal:52844 \
                          --token="$K8S_TOKEN" \
                          --insecure-skip-tls-verify=true \
                          rollout status deployment/task-manager \
                          --timeout=120s
                    '''
                }
            }
        }
    }
}
=======
pipeline {
    agent any

    stages {
        stage('Checkout Code') {
            steps {
                echo 'Checking out Task Manager source code'
                checkout scm
            }
        }

        stage('Build') {
            steps {
                echo 'Building Task Manager Docker image'
                sh 'docker build -t gokul141006/task-manager:v1 .'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKER_USER',
                        passwordVariable: 'DOCKER_TOKEN'
                    )
                ]) {
                    sh '''
                        set +x
                        echo "$DOCKER_TOKEN" | docker login \
                          -u "$DOCKER_USER" --password-stdin
                        docker push gokul141006/task-manager:v1
                        docker logout
                    '''
                }
            }
        }
    }
}
>>>>>>> Stashed changes
