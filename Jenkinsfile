pipeline {
    agent any
    stages {
        stage('Install prerequisites') {
            steps {
                sh '''
                   sudo -H pip install --upgrade pip
                   sudo -H pip install pytest
                   sudo -H pip install databricks-cli
                   python --version
                   cat > ~/.databrickscfg <<EOF
                   [DEFAULT]
                   host = https://adb-3355368943779169.9.azuredatabricks.net
                   token = "danpi6362231bc552a069325527f3ecedcca3d"
                   EOF
               '''
            }
        }
        stage("Checkout") {
            steps {
              checkout scm
              git branch: "main",
                  url: 'https://github.com/cloudstateu/databricks-jenkins.git'
            }
        }
        stage('Run Unit Tests') {
            steps {
                sh "python --version"
                sh "sudo -H python -m pytest https://github.com/cloudstateu/databricks-jenkins/tree/main/uTests/*"
            }
        }
        stage('Import prod notebooks') {
            steps {
                sh "databricks workspace import_dir -o https://github.com/cloudstateu/databricks-jenkins/tree/main/notebooks /Prod"
            }
        }
    }
}