pipeline {
    agent any

    environment {
        SONARQUBE_SERVER = 'SONARQUBE'   // Jenkins SonarQube configuration name
        SONAR_PROJECT_KEY = 'tf-website-monitor'
        SONAR_PROJECT_NAME = 'tf-website-monitor'
        SONAR_HOST_URL = 'http://44.251.129.5:9000'
        SCANNER_TOOL = 'SonarQubeScanner' // Name of SonarQube Scanner tool in Jenkins Global Tool Configuration
    }

    stages {

        stage('SonarQube Code Quality Scan') {
            steps {
                script {
                    withSonarQubeEnv(SONARQUBE_SERVER) {
                        // Use Jenkins-managed SonarQube Scanner tool
                        def scannerHome = tool SCANNER_TOOL

                        // Build scanner command with PR/branch context
                        def scannerCmd = "${scannerHome}/bin/sonar-scanner " +
                            "-Dsonar.projectKey=${SONAR_PROJECT_KEY} " +
                            "-Dsonar.projectName=${SONAR_PROJECT_NAME} " +
                            "-Dsonar.sources=. " +
                            "-Dsonar.host.url=${SONAR_HOST_URL} " +
                            "-Dsonar.login=${SONAR_AUTH_TOKEN}"

                        if (env.CHANGE_ID) {
                            // PR context (e.g., GitHub/GitLab/Bitbucket Multibranch)
                            scannerCmd += " " +
                                "-Dsonar.pullrequest.key=${env.CHANGE_ID} " +
                                "-Dsonar.pullrequest.branch=${env.CHANGE_BRANCH} " +
                                "-Dsonar.pullrequest.base=${env.CHANGE_TARGET}"
                        } else if (env.BRANCH_NAME) {
                            // Branch analysis for non-PR builds
                            scannerCmd += " -Dsonar.branch.name=${env.BRANCH_NAME}"
                        }

                        sh scannerCmd
                    }
                }
            }
        }

        stage("Quality Gate") {
            steps {
                timeout(time: 2, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }
    }

    post {
        success {
            echo 'SonarQube scan passed and quality gate OK!'
        }
        failure {
            echo 'SonarQube scan failed or quality gate failed!'
        }
    }
}
