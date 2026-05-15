pipeline {

    agent any

    stages {

        stage('Clone Repository') {

            steps {

                git 'https://github.com/Vignesh-D18/library-devops-project'

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