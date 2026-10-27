
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
