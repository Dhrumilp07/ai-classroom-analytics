pipeline {
    agent any

    stages {

        stage('Install Dependencies') {
            steps {
                echo 'Installing dependencies'
            }
        }

        stage('Run Test') {
            steps {
                echo 'Pipeline is working!'
            }
        }

        stage('Check Python') {
            steps {
                bat '"C:\\Users\\Dhrumil Patel\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" --version'
            }
        }

    }
}