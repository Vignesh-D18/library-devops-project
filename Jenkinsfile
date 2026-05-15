pipeline {

    agent any

    stages {

        stage('Stop Old Containers') {

            steps {

                bat 'docker-compose down'

            }

        }

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