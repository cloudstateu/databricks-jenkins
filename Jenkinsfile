pipeline {
    agent any
    stages {
        stage('Install prerequisites') {
            steps {
                sh '''
                    pip install --upgrade pip
                    pip install pytest
                    pip install databricks-cli
                    cat > ~/.databrickscfg <<EOF
                    [DEFAULT]
                    host = ${HostUrl}
                    token = dapi64bb8c81c6335d14404f5c4b23e7e78c
EOF
                '''
            }
        }
        stage("Checkout") {
            steps {
              git branch: "main",
                  url: ${GithubUrl}
            }
        }
        stage('Import prod notebooks') {
            steps {
                sh "databricks workspace import_dir -o /var/lib/jenkins/workspace/${env.JOB_NAME}/notebooks/* /Prod"
            }
        }
        stage('Run Unit Tests') {
            steps {
                sh "python3.7 -m pytest /var/lib/jenkins/workspace/${env.JOB_NAME}/uTests/*"
            }
        }
    }
}