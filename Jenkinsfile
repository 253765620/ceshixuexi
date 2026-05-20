def testResult = null

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
                script {
                    testResult = junit 'test-results.xml'
                }
            }
        }
    }

    post {
        always {
            echo 'Tests finished.'
            script {
                def total = testResult?.totalCount ?: 'N/A'
                def passed = testResult?.passCount ?: 'N/A'
                def failed = testResult?.failCount ?: 'N/A'

                def status = currentBuild.result ?: 'SUCCESS'
                def color = (status == 'SUCCESS') ? 'green' : 'red'

                def msg = """\
                    |# ${env.JOB_NAME} - 构建 #${env.BUILD_NUMBER}
                    |
                    |> 状态: <font color="${color}">${status}</font>
                    |> 总计: **${total}** | 通过: **${passed}** | 失败: **${failed}**
                    |> 分支: ${env.BRANCH_NAME}
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
