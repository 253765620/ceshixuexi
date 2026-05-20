pipeline {
    agent any

    environment {
        PYTHON = 'C:\\Users\\25376\\AppData\\Local\\Programs\\Python\\Python39\\python.exe'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Pulling code from Git...'
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing pytest...'
                bat "${env.PYTHON} -m pip install pytest -q"
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running test suite...'
                bat "${env.PYTHON} -m pytest test_calculator.py -v --junitxml=test-results.xml"
            }
        }

        stage('Publish Results') {
            steps {
                echo 'Publishing test report...'
                junit 'test-results.xml'
            }
        }
    }

    post {
        always {
            echo 'Tests finished.'
        }
        success {
            echo 'All tests passed!'
        }
        failure {
            echo 'Some tests failed. Check the report.'
        }
    }
}
