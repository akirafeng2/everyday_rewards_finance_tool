pipeline{
    
    agent any

    stages {
        stage('Checkout Git Repository') {
            steps {
                // Use the 'git' step to clone the repository
                git url: 'https://github.com/akirafeng2/everyday_rewards_finance_tool.git', branch: 'aws-release', credentialsId: 'git-email'
            }
        }

        stage('Connect to ECR') {
            steps {
                script {
                    sh 'aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws/r9z0m9j3'
                }
            }
        }

        stage('Building and push backend image') {
            steps {
                script {
                    sh 'docker build -t finance-app-backend ./src/backend'
                    sh 'docker tag finance-app-backend:latest public.ecr.aws/r9z0m9j3/finance-app-backend:latest'
                    sh 'docker push public.ecr.aws/r9z0m9j3/finance-app-backend:latest'
                }
            }
        }

        stage('Building and push scraper image') {
            steps {
                script {
                    sh 'docker build -t finance-app-scraper ./src/scraper'
                    sh 'docker tag finance-app-scraper:latest public.ecr.aws/r9z0m9j3/finance-app-scraper:latest'
                    sh 'docker push public.ecr.aws/r9z0m9j3/finance-app-scraper:latest'
                }
            }
        }
    }
}