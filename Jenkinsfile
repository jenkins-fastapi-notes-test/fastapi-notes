pipeline {
    agent any

    environment {
        VENV_DIR = ".venv"
        DEV_EMAILS = "aram.cardenas84@gmail.com"
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

        stage('Deploy') {
            steps {
                echo 'Simulating deployment...'
                bat """
                call %VENV_DIR%\\Scripts\\activate
                echo Starting simulated deployment
                uvicorn --app-dir app main:app --reload
                """
            }
        }

        stage('Declarative: Post Actions') {
            steps {
                echo 'Pipeline finished. Sending notifications...'
                script {
                    if (env.CHANGE_ID) {
                        emailext(
                            to: "${DEV_EMAILS}",
                            subject: "Build ${currentBuild.fullDisplayName} finished",
                            body: "The build ${currentBuild.fullDisplayName} has finished with status ${currentBuild.currentResult}."
                        )
                    } else {
                        echo "Not a PR build, skipping email."
                    }
                }
            }
        }
    }

    post {
        success {
            script {
                echo 'Pipeline succeeded.'
                def checkName = env.CHANGE_ID ? 'continuous-integration/jenkins/pr-head' : 'continuous-integration/jenkins/branch'
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
                def checkName = env.CHANGE_ID ? 'continuous-integration/jenkins/pr-head' : 'continuous-integration/jenkins/branch'
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
