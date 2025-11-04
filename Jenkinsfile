pipeline {
    agent any
    
    environment {
        SONAR_PROJECT_KEY = 'tf-website-monitor'
        SONAR_HOST_URL = 'http://44.251.129.5:9000'
    }
    
    stages {
        stage('SonarQube Analysis & Quality Gate') {
            steps {
                withCredentials([string(credentialsId: 'SonarQube', variable: 'SONAR_AUTH_TOKEN'),
                                 string(credentialsId: 'github-token', variable: 'GITHUB_TOKEN')]) {
                    script {
                        // Mark PR status as pending
                        if (env.CHANGE_ID) {
                            githubNotify context: 'SonarQube Quality Gate', 
                                         status: 'PENDING', 
                                         description: 'Running code quality scan...', 
                                         credentialsId: 'github-token'
                        }
                        
                        // Run SonarQube scanner
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

                        // Wait for Quality Gate
                        timeout(time: 5, unit: 'MINUTES') {
                            def qg = waitForQualityGate()
                            echo "Quality Gate Status: ${qg.status}"
                            
                            if (env.CHANGE_ID) {
                                def ghStatus = (qg.status == 'OK') ? 'SUCCESS' : 'FAILURE'
                                githubNotify context: 'SonarQube Quality Gate', 
                                             status: ghStatus, 
                                             description: "Quality gate ${qg.status}", 
                                             credentialsId: 'github-token'
                            }
                            
                            if (qg.status != 'OK') {
                                error "Pipeline aborted due to Quality Gate failure: ${qg.status}"
                            }
                        }
                    }
                }
            }
        }
    }
}
