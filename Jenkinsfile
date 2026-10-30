pipeline {
    agent any

    environment {
        IMAGE_NAME = 'myapp'
        IMAGE_TAG  = "${env.BUILD_NUMBER}"
        RELEASE    = 'myapp'
        NAMESPACE  = 'dev'
        CHART_DIR  = 'helm/myapp'
    }

    stages {
        stage('Checkout') {
            steps { checkout scm }
        }

        stage('Lint Helm Chart') {
            steps {
                sh 'helm lint ${CHART_DIR} -f ${CHART_DIR}/values-dev.yaml'
                sh 'helm template ${RELEASE} ${CHART_DIR} -f ${CHART_DIR}/values-dev.yaml > /dev/null'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t ${IMAGE_NAME}:${IMAGE_TAG} app/'
            }
        }

        stage('Deploy with Helm') {
            steps {
                sh '''
                  helm upgrade --install ${RELEASE} ${CHART_DIR} \
                    -n ${NAMESPACE} --create-namespace \
                    -f ${CHART_DIR}/values-dev.yaml \
                    --set image.repository=${IMAGE_NAME} \
                    --set image.tag=${IMAGE_TAG} \
                    --wait --timeout 120s
                '''
            }
        }

        stage('Verify') {
            steps {
                sh 'kubectl get pods -n ${NAMESPACE}'
                sh 'helm status ${RELEASE} -n ${NAMESPACE}'
            }
        }
    }

    post {
        failure {
            echo 'Deployment failed - rolling back'
            sh 'helm rollback ${RELEASE} -n ${NAMESPACE} || true'
        }
    }
}
