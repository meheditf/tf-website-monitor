pipeline {
    agent any
    stages {
        stage('Test Credential') {
            steps {
                withCredentials([string(credentialsId: 'SonarQube', variable: 'TEST_TOKEN')]) {
                    sh 'echo "Token length: ${#TEST_TOKEN}"'
                }
            }
        }
    }
}
