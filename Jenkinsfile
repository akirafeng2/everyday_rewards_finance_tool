pipeline{
    
    agent any

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
                    // Define your Docker Compose command here
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