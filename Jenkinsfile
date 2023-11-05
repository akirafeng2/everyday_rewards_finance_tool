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
                git url: 'https://github.com/akirafeng2/everyday_rewards_finance_tool.git', branch: 'main', credentialsId: 'token'
            }
        }
        stage('Conditional Build and Run Docker Compose') {
            when {
                expression {
                    // This stage will only run when the pull request is merged into the main branch
                    currentBuild.changeSets.any { it.branch == 'main' }
                }
            }
            steps {
                script {
                    // Define your Docker Compose command here
                    def dockerComposeCmd = "docker-compose up --build"

                    // Execute the Docker Compose command
                    sh(script: dockerComposeCmd, returnStatus: true)

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