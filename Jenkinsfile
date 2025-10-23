pipeline {
    agent any

    environment {
        VENV_DIR = ".venv"
        DEV_EMAILS = "aram.cardenas84@gmail.com" // Replace with real PR email group
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
        always {
            echo 'Pipeline finished.'
        }

        success {
            script {
                handleBuildStatus('SUCCESS', '✅ Build passed')
            }
        }

        failure {
            script {
                handleBuildStatus('FAILURE', '❌ Build failed')
            }
        }
    }
}

// Helper function to reduce duplication
def handleBuildStatus(conclusion, summary) {
    def checkName = env.CHANGE_ID ? 'continuous-integration/jenkins/pr-head' : 'continuous-integration/jenkins/branch'

    publishChecks(
        name: checkName,
        title: 'Build Status',
        summary: summary,
        conclusion: conclusion
    )

    // Send email only if this is a PR
    if (env.CHANGE_ID) {
        emailext(
            subject: "Jenkins PR Build ${conclusion}: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
            body: """
                Jenkins build ${env.JOB_NAME} #${env.BUILD_NUMBER} has ${conclusion}.
                Check console output at ${env.BUILD_URL} for details.
            """,
            to: env.DEV_EMAILS
        )
    }
}
