pipeline {
    agent any

    stages {

        stage('Checkout Source') {
            steps {
                checkout scm
            }
        }

        stage('Verify Python') {
            steps {
                sh 'python3 --version'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip3 install -r requirements.txt'
            }
        }

        stage('Run Storage Automation') {
            steps {
                sh 'python3 src/main.py'
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'output/**/*.xlsx', fingerprint: true
        }

        success {
            echo 'Build Successful!'
        }

        failure {
            echo 'Build Failed!'
        }
    }
}