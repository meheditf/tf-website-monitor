pipeline {
    agent any

    environment {
        SONAR_PROJECT_KEY = 'tf-website-monitor'
        SONAR_HOST_URL = 'http://44.251.129.5:9000'
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout code (PR or branch)
                checkout scm
            }
        }

        stage('SonarQube Code Quality Scan') {
            steps {
                withCredentials([string(credentialsId: 'SonarQube', variable: 'SONAR_AUTH_TOKEN')]) {
                    script {
                        // Detect PR info
                        def prId = env.CHANGE_ID ?: ""
                        def prBranch = env.CHANGE_BRANCH ?: env.BRANCH_NAME
                        def targetBranch = env.CHANGE_TARGET ?: "dev"

                        // Run SonarQube scan
                        sh """
                        /usr/local/bin/sonar-scanner \
                            -Dsonar.projectKey=${SONAR_PROJECT_KEY} \
                            -Dsonar.projectName=${SONAR_PROJECT_KEY} \
                            -Dsonar.sources=. \
                            -Dsonar.host.url=${SONAR_HOST_URL} \
                            -Dsonar.login=${SONAR_AUTH_TOKEN} \
                            -Dsonar.python.version=3 \
                            ${prId ? "-Dsonar.pullrequest.key=${prId} -Dsonar.pullrequest.branch=${prBranch} -Dsonar.pullrequest.base=${targetBranch}" : ""}
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
                        // Post status to GitHub PR
                        def status = qg.status == 'OK' ? 'SUCCESS' : 'FAILURE'
                        def description = "SonarQube Quality Gate: ${qg.status}"

                        // Only post if this is a PR
                        if (env.CHANGE_ID) {
                            githubNotify status: status,
                                         description: description,
                                         context: 'SonarQube'
                        }

                        if (qg.status != 'OK') {
                            error "❌ Pipeline aborted due to Quality Gate failure: ${qg.status}"
                        }
                    }
                }
            }
        }
    }

    post {
        success {
            echo '✅ SonarQube scan passed and Quality Gate OK!'
        }
        failure {
            echo '❌ SonarQube scan failed or Quality Gate failed!'
        }
    }
}
