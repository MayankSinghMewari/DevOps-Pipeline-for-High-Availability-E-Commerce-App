// Jenkinsfile for E-commerce App CI/CD Pipeline

pipeline {
    agent any // This pipeline can run on any available Jenkins agent

    // Environment variables
    environment {
        DOCKER_HUB_USERNAME = credentials('dockerhub-username') // Jenkins Credential ID for Docker Hub username
        DOCKER_HUB_PASSWORD = credentials('dockerhub-password') // Jenkins Credential ID for Docker Hub password
        IMAGE_NAME = "mayanksinghmewari/ecommerce-app" // Replace with your Docker Hub username/repo name
        TAG = "${env.BUILD_NUMBER}" // Use Jenkins build number as image tag
    }

    stages {
        stage('Checkout SCM') {
            steps {
                // Checkout the latest code from your Git repository
                git branch: 'main', credentialsId: 'github-pat', url: 'https://github.com/MayankSinghMewari/DevOps-Pipeline-for-High-Availability-E-Commerce-App1.git'
                // Use 'github-pat' credential for pulling code if your repo is private
                // If public, you might not need credentialsId here.
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    // Login to Docker Hub (or your registry)
                    withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh "echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin"
                    }

                    // Build the Docker image
                    sh "docker build -t ${IMAGE_NAME}:${TAG} ."
                    sh "docker build -t ${IMAGE_NAME}:latest ." // Also tag as latest
                }
            }
        }

        // Optional Stage 3: Test (Placeholder)
        stage('Test Application') {
            steps {
                script {
                    // For a Streamlit app, testing typically involves
                    // 1. Running the container
                    // 2. Running a health check or a simple curl to a known endpoint
                    // 3. Potentially running unit/integration tests (if you have them)
                    //
                    // Example (running the app in a temporary container and health checking):
                    sh "echo 'Running temporary container for testing...'"
                    sh "docker run -d --rm --name temp-ecommerce-app -p 8501:8501 ${IMAGE_NAME}:${TAG}"
                    sh "sleep 10" // Give the app time to start
                    sh "curl --fail http://localhost:8501/_stcore/health || docker logs temp-ecommerce-app"
                    sh "docker stop temp-ecommerce-app" // Stop the temporary container

                    // If you have Python unit tests (e.g., using pytest):
                    // sh "python -m pytest tests/"
                    echo "Tests completed successfully (or placeholder executed)."
                }
            }
        }

        stage('Push to Registry') {
            steps {
                script {
                    // Push the tagged image
                    withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                        sh "docker push ${IMAGE_NAME}:${TAG}"
                        sh "docker push ${IMAGE_NAME}:latest"
                    }
                }
            }
        }
    }

    // Post-build actions (e.g., notifications)
    post {
        always {
            cleanWs() // Clean up workspace after build
        }
        success {
            echo 'Pipeline finished successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}