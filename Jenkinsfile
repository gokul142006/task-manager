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
                sh 'docker build -t task-manager:v1 .'
            }
        }
    }
}
