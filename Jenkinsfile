pipeline {
    agent any
    stages {
        stage('Install prerequisites') {
            steps {
                sh '''
                    python3.7 -m venv venv
                    source venv/bin/activate
                    pip install --upgrade pip
                    pip install pytest
                    pip install databricks-cli
                    cat > ~/.databrickscfg <<EOF
                    [DEFAULT]
                    host = https://adb-3355368943779169.9.azuredatabricks.net
                    token = dapi64bb8c81c6335d14404f5c4b23e7e78c
EOF
                '''
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
                sh "databricks workspace mkdirs /Users/daniel.pisarek@chmurowisko.pl/MyNewFolder"
                sh "databricks workspace import_dir -o /var/lib/jenkins/workspace/cloudstate-databricksTestPipeline/notebooks/* /Prod"
            }
        }
        stage('Run Unit Tests') {
            steps {
                sh "python3 --version"
                sh "python3 -m pytest /var/lib/jenkins/workspace/cloudstate-databricksTestPipeline/uTests/*"
                sh "deactivate"
            }
        }
    }
}