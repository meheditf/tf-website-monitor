pipeline {
    agent any
    
    environment {
        SONAR_PROJECT_KEY = 'tf-website-monitor'
        SONAR_HOST_URL = 'http://44.251.129.5:9000'
        GITHUB_STATUS_CONTEXT = 'SonarQube Quality Gate'
    }
    
    stages {
        stage('Debug Info') {
            steps {
                script {
                    echo "=== BUILD DEBUG INFORMATION ==="
                    echo "Build Number: ${env.BUILD_NUMBER}"
                    echo "Job Name: ${env.JOB_NAME}"
                    echo "Branch Name: ${env.BRANCH_NAME ?: 'N/A'}"
                    echo "Change ID (PR Number): ${env.CHANGE_ID ?: 'N/A'}"
                    echo "Change URL: ${env.CHANGE_URL ?: 'N/A'}"
                    echo "Change Branch: ${env.CHANGE_BRANCH ?: 'N/A'}"
                    echo "Change Target: ${env.CHANGE_TARGET ?: 'N/A'}"
                    echo "GIT Branch: ${env.GIT_BRANCH ?: 'N/A'}"
                    echo "Is this a PR build? ${env.CHANGE_ID ? 'YES' : 'NO'}"
                    echo "================================"
                }
            }
        }
        
        stage('SonarQube Analysis & Quality Gate') {
            steps {
                script {
                    withCredentials([
                        string(credentialsId: 'SonarQube', variable: 'SONAR_AUTH_TOKEN'),
                        string(credentialsId: 'github-token', variable: 'GITHUB_TOKEN')
                    ]) {
                        // Mark PR status as pending
                        if (env.CHANGE_ID) {
                            echo "=== Setting GitHub status to PENDING for PR #${env.CHANGE_ID} ==="
                            echo "PR URL: ${env.CHANGE_URL}"
                            echo "Status context name: '${env.GITHUB_STATUS_CONTEXT}'"
                            try {
                                setGitHubPullRequestStatus(
                                    context: env.GITHUB_STATUS_CONTEXT,
                                    state: 'PENDING',
                                    message: 'Running code quality scan...'
                                )
                                echo "✓ GitHub status notification sent successfully"
                            } catch (Exception e) {
                                echo "✗ WARNING: Failed to set GitHub status: ${e.message}"
                                e.printStackTrace()
                            }
                        } else {
                            echo "Not a PR build (CHANGE_ID is null), skipping GitHub status notification"
                        }
                        
                        // Run SonarQube scanner
                        echo "=== Running SonarQube Analysis ==="
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
                        echo "=== Waiting for SonarQube Quality Gate result ==="
                        timeout(time: 5, unit: 'MINUTES') {
                            def qg = waitForQualityGate()
                            echo "Quality Gate Status: ${qg.status}"
                            
                            if (env.CHANGE_ID) {
                                def ghState = (qg.status == 'OK') ? 'SUCCESS' : 'FAILURE'
                                def ghMessage = (qg.status == 'OK') ? 
                                    'Quality gate passed ✓' : 
                                    "Quality gate failed: ${qg.status}"
                                
                                echo "=== Setting GitHub status to ${ghState} for PR #${env.CHANGE_ID} ==="
                                echo "Status context name: '${env.GITHUB_STATUS_CONTEXT}'"
                                echo "Message: ${ghMessage}"
                                try {
                                    setGitHubPullRequestStatus(
                                        context: env.GITHUB_STATUS_CONTEXT,
                                        state: ghState,
                                        message: ghMessage
                                    )
                                    echo "✓ GitHub status notification sent successfully: ${ghState}"
                                } catch (Exception e) {
                                    echo "✗ WARNING: Failed to set GitHub status: ${e.message}"
                                    e.printStackTrace()
                                }
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
    
    post {
        failure {
            script {
                echo "=== Pipeline FAILED ==="
                if (env.CHANGE_ID) {
                    echo "Setting GitHub status to FAILURE for PR #${env.CHANGE_ID}"
                    withCredentials([string(credentialsId: 'github-token', variable: 'GITHUB_TOKEN')]) {
                        try {
                            setGitHubPullRequestStatus(
                                context: env.GITHUB_STATUS_CONTEXT,
                                state: 'FAILURE',
                                message: 'Pipeline execution failed'
                            )
                            echo "✓ GitHub failure status sent"
                        } catch (Exception e) {
                            echo "✗ WARNING: Failed to set GitHub failure status: ${e.message}"
                            e.printStackTrace()
                        }
                    }
                } else {
                    echo "Not a PR build, skipping GitHub status notification"
                }
            }
        }
        success {
            echo "=== Pipeline SUCCEEDED ==="
        }
    }
}