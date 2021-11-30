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
                echo "Jenkins job piotr!"
                echo "Model name is: ${params.modelname}, model version is: ${params.modelversion}"
            }
        }
    }
}