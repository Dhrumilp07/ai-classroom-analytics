pipeline {
    agent any

    stages {

        stage('Clone Repo') {
            steps {
                git 'https://github.com/Dhrumil07/ai-classroom-analytics.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run App Test') {
            steps {
                sh 'python --version'
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t ai-classroom-analytics .'
            }
        }

    }
}
