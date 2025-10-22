pipeline {
    agent any

    environment {
        VENV_DIR = ".venv"
    }

    stages {
        stage('Build') {
            steps {
                echo 'Creating virtual environment and installing dependencies...'
                bat """
                set PYTHONPATH=%CD%
                python -m venv %VENV_DIR%
                call %VENV_DIR%\\Scripts\\activate
                pip install --upgrade pip
                pip install -r requirements.txt
                """
            }
        }

        stage('Test') {
            steps {
                echo 'Running unit tests with coverage...'
                bat """
                set PYTHONPATH=%CD%
                call %VENV_DIR%\\Scripts\\activate
                pytest --cov=app --cov-report=term-missing --maxfail=1 --disable-warnings -q
                """
            }
        }
    }

    post {
        success {
            script {
                echo 'Pipeline succeeded.'

                // Detect whether this is a PR or a branch build
                def checkName = env.CHANGE_ID ? 
                    'continuous-integration/jenkins/pr-head' : 
                    'continuous-integration/jenkins/branch'

                publishChecks(
                    name: checkName,
                    title: 'Build Status',
                    summary: '✅ Build passed',
                    conclusion: 'SUCCESS'
                )
            }
        }

        failure {
            script {
                echo 'Pipeline failed.'

                def checkName = env.CHANGE_ID ? 
                    'continuous-integration/jenkins/pr-head' : 
                    'continuous-integration/jenkins/branch'

                publishChecks(
                    name: checkName,
                    title: 'Build Status',
                    summary: '❌ Build failed',
                    conclusion: 'FAILURE'
                )
            }
        }

        always {
            echo 'Pipeline finished.'
        }
    }
}
