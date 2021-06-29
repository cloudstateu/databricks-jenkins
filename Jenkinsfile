pipeline {
    agent { docker { image 'ubuntu:latest' } }
    stages {
        stage('Install prerequisites') {
            steps {
                sh '''
                   python -m pip install --upgrade pip
                   pip install pytest
                   pip install databricks-cli
                   cat > ~/.databrickscfg <<EOF
                   [DEFAULT]
                   host = https://adb-3355368943779169.9.azuredatabricks.net
                   token = $(echo "${{ secrets.DATABRICKS_TOKEN }}")
                   EOF
               '''
            }
        }
        stage('Github checkout') {
            steps {
                git url: "https://github.com/cloudstateu/databricks-jenkins.git"
            }
        }
        stage('Run Unit Tests') {
            steps {
                sh "python -m pytest https://github.com/cloudstateu/databricks-jenkins/tree/main/uTests/*"
            }
        }
        stage('Import prod notebooks') {
            steps {
                sh "databricks workspace import_dir -o https://github.com/cloudstateu/databricks-jenkins/tree/main/notebooks /Prod"
            }
        }
    }
}