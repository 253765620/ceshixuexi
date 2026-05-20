pipeline {
    agent any

    environment {
        PYTHON = 'C:\\Users\\25376\\AppData\\Local\\Programs\\Python\\Python39\\python.exe'
        SENDKEY = 'SCT352402T5740VJf0G3TdpltsoyAGb9pq'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Pulling code from Git...'
                checkout scm
                script {
                    env.MY_BRANCH = env.GIT_BRANCH?.replace('origin/', '') ?: 'main'
                }
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
            script {
                def total = 'N/A'
                def passed = 'N/A'
                def failed = 'N/A'
                try {
                    def action = currentBuild.rawBuild.getAction(hudson.tasks.junit.TestResultAction.class)
                    if (action != null) {
                        total = action.totalCount
                        passed = action.passCount
                        failed = action.failCount
                    }
                } catch (e) {
                    echo "Failed to read test results: ${e.message}"
                }

                def status = currentBuild.result ?: 'SUCCESS'
                def color = (status == 'SUCCESS') ? 'green' : 'red'
                def branch = env.MY_BRANCH ?: 'main'

                def msg = """\
                    |# ${env.JOB_NAME} - 构建 #${env.BUILD_NUMBER}
                    |
                    |> 状态: <font color="${color}">${status}</font>
                    |> 总计: **${total}** | 通过: **${passed}** | 失败: **${failed}**
                    |> 分支: ${branch}
                    |> [查看详情](${env.BUILD_URL})
                    """.stripMargin()

                powershell """
                    \$body = @{
                        title = '${env.JOB_NAME} #${env.BUILD_NUMBER} - ${status}'
                        desp = @'
${msg}
'@
                    }
                    Invoke-RestMethod -Uri 'https://sctapi.ftqq.com/${env.SENDKEY}.send' \
                        -Method Post -Body \$body
                """
            }
        }
    }
}
