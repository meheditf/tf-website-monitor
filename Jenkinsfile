pipeline {
    agent any
    
    environment {
        SONAR_PROJECT_KEY = 'tf-website-monitor'
        SONAR_HOST_URL = 'http://44.251.129.5:9000'
    }
    
    stages {
        stage('SonarQube Analysis & Quality Gate') {
            steps {
                script {
                    // Set GitHub status to pending (if this is a PR)
                    if (env.CHANGE_ID) {
                        try {
                            githubNotify status: 'PENDING', 
                                         context: 'SonarQube Quality Gate',
                                         description: 'Running code quality scan...'
                        } catch (Exception e) {
                            echo "Warning: Could not update GitHub status: ${e.message}"
                        }
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
                            -Dsonar.token=${SONAR_AUTH_TOKEN} \
                            -Dsonar.python.version=3.12
                        """
                    }
                    
                    // Wait for quality gate - OUTSIDE withSonarQubeEnv but INSIDE withCredentials
                    timeout(time: 5, unit: 'MINUTES') {
                        script {
                            echo "Waiting for SonarQube Quality Gate result..."
                            
                            try {
                                def qg = waitForQualityGate()
                                echo "Quality Gate Status: ${qg.status}"
                                
                                if (qg.status != 'OK') {
                                    // Update GitHub with failure
                                    if (env.CHANGE_ID) {
                                        try {
                                            githubNotify status: 'FAILURE',
                                                         context: 'SonarQube Quality Gate',
                                                         description: "Quality gate failed: ${qg.status}"
                                        } catch (Exception e) {
                                            echo "Warning: Could not update GitHub status: ${e.message}"
                                        }
                                    }
                                    error "Pipeline aborted due to quality gate failure: ${qg.status}"
                                } else {
                                    // Update GitHub with success
                                    if (env.CHANGE_ID) {
                                        try {
                                            githubNotify status: 'SUCCESS',
                                                         context: 'SonarQube Quality Gate',
                                                         description: 'Quality gate passed!'
                                        } catch (Exception e) {
                                            echo "Warning: Could not update GitHub status: ${e.message}"
                                        }
                                    }
                                }
                            } catch (Exception e) {
                                echo "ERROR waiting for Quality Gate: ${e.message}"
                                echo "This usually means the webhook from SonarQube didn't arrive"
                                throw e
                            }
                        }
                    }
                }
            }
        }
    }                
    
    post {
        success {
            script {
                githubNotify context: 'Jenkins', status: 'SUCCESS', description: 'Build and SonarQube passed'
            }
        }
        failure {
            script {
                githubNotify context: 'Jenkins', status: 'FAILURE', description: 'SonarQube Quality Gate failed'
            }
        }
    }
}
