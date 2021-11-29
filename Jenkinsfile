pipeline {
    agent any
    stages {
        stage('Import notebook') {
            steps {
                sh "whoami"
            }
        }
        stage('Update databricks job') {
            steps {
                sh '''
                echo "Jenkins job piotr!"
                ls
                '''
            }
        }
    }
}