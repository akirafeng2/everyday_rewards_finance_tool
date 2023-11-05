pipeline{
    
    agent any

    environment {
        ENV = 'prod'
        IP_ADDRESS = '192.168.0.8'
        DB_NAME = 'finance_prod'
        USER = 'root'
        PASSWORD = 'root'
        HOST = '192.168.0.8'
        PORT = '5432'
        SECRET_KEY = 'my_secret_key'
    }

    stages {
        stage('Checkout Git Repository') {
            steps {
                // Use the 'git' step to clone the repository
                git url: 'https://github.com/akirafeng2/everyday_rewards_finance_tool.git', branch: 'main', credentialsId: 'git-email'
            }
        }
        stage('Run Docker Compose') {
            steps {
                script {
                    sh 'docker-compose up --build -d'

                    if (currentBuild.resultIsBetterOrEqualTo('SUCCESS')) {
                        echo "Docker Compose executed successfully."
                    } else {
                        error "Docker Compose command failed."
                    }
                }
            }
        }
    }
}