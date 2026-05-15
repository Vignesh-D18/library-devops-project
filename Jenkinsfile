pipeline {

    agent any

    stages {

        stage('Clone Repository') {

            steps {

                git 'YOUR_GITHUB_REPOSITORY_URL'

            }

        }

        stage('Build Docker Containers') {

            steps {

                sh 'docker-compose build'

            }

        }

        stage('Deploy Containers') {

            steps {

                sh 'docker-compose up -d'

            }

        }

    }

}