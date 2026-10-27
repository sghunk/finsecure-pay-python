pipeline {
    agent any
    environment {
        IMAGE_NAME = 'finsecure-api'
        IMAGE_TAG  = 'v1.0.0'
    }
    stages {
        stage('Checkout Source') {
            steps {
                echo 'Pulling application scripts from repository source control...'
                checkout scm
            }
        }
        stage('Static Code Quality Analysis') {
            steps {
                echo 'Running Python Static Analysis Code Scanning...'
                sh 'pip install pylint && pylint --errors-only automation.py'
            }
        }
        stage('Automated Regression Testing') {
            steps {
                echo 'Executing pytest validation test cases...'
                sh 'pip install -r requirements.txt && pytest -v'
            }
        }
        stage('Dependency Vulnerability Audit') {
            steps {
                echo 'Scanning requirements.txt for outdated or insecure libraries...'
                sh 'pip install pip-audit && pip-audit'
            }
        }
        stage('Compile and Build Image') {
            steps {
                echo 'Assembling project layers into Docker storage container...'
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
            }
        }
        stage('Orchestrate Deployment Update') {
            steps {
                echo 'Applying manifest updates into the active Kubernetes cluster...'
                sh 'kubectl apply -f configmap.yaml'
                sh 'kubectl apply -f deployment.yaml'
            }
        }
    }
}
