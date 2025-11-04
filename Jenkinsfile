pipeline {
    agent any
    
    environment {
        SONAR_PROJECT_KEY = 'tf-website-monitor'
        SONAR_HOST_URL = 'http://44.251.129.5:9000'
    }
    
    stages {
        stage('SonarQube Code Quality Scan') {
            steps {
                // Set GitHub status to pending
                script {
                    if (env.CHANGE_ID) {
                        githubNotify status: 'PENDING', 
                                     context: 'SonarQube Quality Gate',
                                     description: 'Running code quality scan...'
                    }
                }
                
                withCredentials([string(credentialsId: 'SonarQube', variable: 'SONAR_AUTH_TOKEN')]) {
                    withSonarQubeEnv('SONARQUBE') {
                        sh """
                            /usr/local/bin/sonar-scanner \
                            -Dsonar.projectKey=${SONAR_PROJECT_KEY} \
                            -Dsonar.projectName=${SONAR_PROJECT_KEY} \
                            -Dsonar.sources=. \
                            -Dsonar.host.url=${SONAR_HOST_URL} \
                            -Dsonar.login=${SONAR_AUTH_TOKEN} \
                            -Dsonar.python.version=3.12
                        """
                    }
                }
            }
        }
        
        stage('Quality Gate') {
            steps {
                timeout(time: 2, unit: 'MINUTES') {
                    script {
                        def qg = waitForQualityGate()
                        if (qg.status != 'OK') {
                            if (env.CHANGE_ID) {
                                githubNotify status: 'FAILURE',
                                             context: 'SonarQube Quality Gate',
                                             description: "Quality gate failed: ${qg.status}"
                            }
                            error "Quality gate failed: ${qg.status}"
                        } else {
                            if (env.CHANGE_ID) {
                                githubNotify status: 'SUCCESS',
                                             context: 'SonarQube Quality Gate',
                                             description: 'Quality gate passed!'
                            }
                        }
                    }
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