pipeline {
    agent any

    environment {
        SONARQUBE_SERVER = 'SONARQUBE'
        SONAR_PROJECT_KEY = 'tf-website-monitor'
        SONAR_HOST_URL = 'http://44.251.129.5:9000'
    }

    stages {
        stage('SonarQube Code Quality Scan') {
            steps {
                withCredentials([string(credentialsId: 'SONARQUBE_AUTH_TOKEN', variable: 'SONAR_AUTH_TOKEN')]) {
                    script {
                        def scannerHome = tool 'SonarQubeScanner'
                        sh """
                            ${scannerHome}/bin/sonar-scanner \
                            -Dsonar.projectKey=${SONAR_PROJECT_KEY} \
                            -Dsonar.sources=. \
                            -Dsonar.host.url=${SONAR_HOST_URL} \
                            -Dsonar.login=${SONAR_AUTH_TOKEN}
                        """
                    }
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 2, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
    }

    post {
        success {
            echo '✅ SonarQube scan passed and quality gate OK!'
        }
        failure {
            echo '❌ SonarQube scan failed or quality gate failed!'
        }
    }
}
