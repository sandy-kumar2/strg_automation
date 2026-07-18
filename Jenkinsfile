pipeline {
    agent any

    stages {

        stage('Verify Python') {
            steps {
                sh 'python3 --version'
            }
        }

        stage('Create Virtual Environment') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Storage Automation') {
            steps {
                sh '''
                    . venv/bin/activate
                    python src/main.py
                '''
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