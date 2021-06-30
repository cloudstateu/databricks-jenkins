pipeline {
    agent { docker 'ubuntu:latest' }
    stages {
        stage('Install prerequisites') {
            steps {
                sh '''
                   sudo apt update
                   sudo apt install software-properties-common
                   sudo add-apt-repository ppa:deadsnakes/ppa
                   sudo apt update
                   sudo apt install python3.8
                   python ––version
                   python3 -m pip install --upgrade pip
                   pip install --upgrade pytest
                   pip install databricks-cli
                   python -m pytest
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