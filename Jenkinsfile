pipeline {
    agent any
    stages {
        stage('Install prerequisites') {
            steps {
                sh '''
                   sudo -H pip install --upgrade pip
                   sudo -H pip install pytest
                   sudo -H pip install databricks-cli
                   cat > ~/.databrickscfg << EOF
                   [DEFAULT]
                   host = https://adb-3355368943779169.9.azuredatabricks.net
                   token = "danpi6362231bc552a06932527f3ecedcca3d"
                   EOF
                   '''.stripIndent()
            }
        }
        stage("Checkout") {
            steps {
              sh "ls"
              sh "pwd"
              checkout scm
              git branch: "main",
                  url: 'https://github.com/cloudstateu/databricks-jenkins'
            }
        }
        stage('Import prod notebooks') {
            steps {
                sh "databricks workspace import_dir -o /var/lib/jenkins/workspace/cloudstate-databricksTestPipeline/notebooks/* /Prod"
            }
        }
        stage('Run Unit Tests') {
            steps {
                sh "python --version"
                sh "python -m pytest https://github.com/cloudstateu/databricks-jenkins/tree/main/uTests/*"
            }
        }
    }
}