pipeline {
    agent any

    environment {
        SONAR_PROJECT_KEY = "${env.JOB_NAME}" // Use job name as project key
        SONAR_HOST_URL = credentials('http://44.251.129.5:9000') // Jenkins credential or global variable

    }

    stages {
        stage('Debug Info') {
            steps {
                echo "=== BUILD DEBUG INFORMATION ==="
                echo "Build Number: ${env.BUILD_NUMBER}"
                echo "Job Name: ${env.JOB_NAME}"
                echo "Branch Name: ${env.BRANCH_NAME ?: 'N/A'}"
                echo "PR Number (CHANGE_ID): ${env.CHANGE_ID ?: 'N/A'}"
                echo "Target Branch (CHANGE_TARGET): ${env.CHANGE_TARGET ?: 'N/A'}"
                echo "Is PR Build? ${env.CHANGE_ID ? 'YES' : 'NO'}"
            }
        }

        stage('SonarQube Analysis & Quality Gate') {
            steps {
                script {
                    // Mark PR status as pending using githubNotify
                    if (env.CHANGE_ID) {
                        githubNotify context: 'SonarQube Quality Gate', status: 'PENDING'
                    }

                    // Run SonarQube scan
                    withSonarQubeEnv('SONARQUBE') {
                        sh """
                            sonar-scanner \
                                -Dsonar.projectKey=${SONAR_PROJECT_KEY} \
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

                        // Update PR status
                        if (env.CHANGE_ID) {
                            def ghState = (qg.status == 'OK') ? 'SUCCESS' : 'FAILURE'
                            githubNotify context: 'SonarQube Quality Gate', status: ghState
                        }

                        if (qg.status != 'OK') {
                            error "Pipeline aborted due to Quality Gate failure: ${qg.status}"
                        }
                    }
                }
            }
        }
    }

    post {
        failure {
            script {
                echo "=== Pipeline FAILED ==="
                if (env.CHANGE_ID) {
                    githubNotify context: 'SonarQube Quality Gate', status: 'FAILURE'
                }
            }
        }
        success {
            echo "=== Pipeline SUCCEEDED ==="
        }
    }
}
