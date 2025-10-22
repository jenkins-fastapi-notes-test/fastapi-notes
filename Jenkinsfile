pipeline {
    agent any

    stages {

        stage('Build') {
            steps {
                echo 'Creating virtual environment and installing dependencies...'
                bat '''
                set PYTHONPATH=%CD%
                python -m venv .venv
                call .venv\\Scripts\\activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                echo 'Running unit tests with coverage...'
                bat '''
                set PYTHONPATH=%CD%
                call .venv\\Scripts\\activate
                pytest --cov=app --cov-report=term-missing --maxfail=1 --disable-warnings -q
                '''
            }
        }
    }

    post {
    success {
        echo 'Pipeline succeeded.'
        githubNotify context: 'jenkins/ci', description: 'Build passed', status: 'SUCCESS'
    }
    failure {
        echo 'Pipeline failed.'
        githubNotify context: 'jenkins/ci', description: 'Build failed', status: 'FAILURE'
    }
    always {
        echo 'Pipeline finished.'
    }
}

}
