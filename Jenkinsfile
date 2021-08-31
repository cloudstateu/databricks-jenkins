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
                    host = ${WorkspaceUrl}
                    token = ${DatabricksToken}
EOF
                '''
            }
        }
        stage('Import notebook') {
            steps {
                sh "databricks workspace import -o -l PYTHON /var/lib/jenkins/workspace/${env.JOB_NAME}/notebooks/holos_analytics_pipeline.py /notebooks/piotr-test.py"
            }
        }
    }
}