pipeline {
    agent any

    environment {
        SONARQUBE_SERVER = 'SONARQUBE'   // Jenkins SonarQube configuration name
        SONAR_PROJECT_KEY = 'tf-website-monitor'
        SONAR_PROJECT_NAME = 'tf-website-monitor'
        SONAR_HOST_URL = 'http://44.251.129.5:9000'
    }

    stages {

        stage('SonarQube Code Quality Scan') {
            steps {
                script {
                    withSonarQubeEnv(SONARQUBE_SERVER) {
                        // Build Sonar command with PR decoration if this is a Multibranch PR build
                        def mvnCmd = "mvn -B clean verify sonar:sonar " +
                            "-Dsonar.projectKey=${SONAR_PROJECT_KEY} " +
                            "-Dsonar.projectName=${SONAR_PROJECT_NAME} " +
                            "-Dsonar.host.url=${SONAR_HOST_URL} " +
                            "-Dsonar.login=${SONAR_AUTH_TOKEN}"

                        if (env.CHANGE_ID) {
                            // PR context (e.g., GitHub/GitLab/Bitbucket Multibranch)
                            mvnCmd += " " +
                                "-Dsonar.pullrequest.key=${env.CHANGE_ID} " +
                                "-Dsonar.pullrequest.branch=${env.CHANGE_BRANCH} " +
                                "-Dsonar.pullrequest.base=${env.CHANGE_TARGET}"
                        } else if (env.BRANCH_NAME) {
                            // Branch analysis for non-PR builds
                            mvnCmd += " -Dsonar.branch.name=${env.BRANCH_NAME}"
                        }

                        sh mvnCmd
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
