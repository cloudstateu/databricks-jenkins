pipeline {
    agent any
    stages {
        stage('Checkout'){
            steps{
                checkout scm
            }
        }
        stage('Install prerequisites') {
            steps {
                sh '''
                    pip install --upgrade pip
                    pip install pytest
                    pip install databricks-cli
                    cat > ~/.databrickscfg <<EOF
                    [DEFAULT]
                    host = ${HostUrl}
                    token = ${DataBricksToken}
EOF
                '''
            }
        }
        stage('Run Unit Tests') {
            steps {
                sh "python3.7 -m pytest /var/lib/jenkins/workspace/${env.JOB_NAME}/uTests/*"
            }
        }
        stage('Import prod notebooks') {
            steps {
                sh "databricks workspace import_dir -o /var/lib/jenkins/workspace/${env.JOB_NAME}/notebooks/* /Prod"
            }
        }
    }
}