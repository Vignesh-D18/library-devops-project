pipeline {

    agent any

    stages {

        stage('Build Docker Containers') {

            steps {

                bat 'docker-compose build'

            }

        }

        stage('Deploy Containers') {

            steps {

                bat 'docker-compose up -d'

            }

        }

    }

}