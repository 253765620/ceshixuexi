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

        stage('Parse Results') {
            steps {
                echo 'Parsing test results...'
                script {
                    def xml = readFile 'test-results.xml'
                    def total = (xml =~ /tests="(\d+)"/)[0][1]
                    def failures = (xml =~ /failures="(\d+)"/)[0][1]
                    def errors = (xml =~ /errors="(\d+)"/)[0][1]
                    def skipped = (xml =~ /skipped="(\d+)"/)[0][1]
                    env.TEST_TOTAL = total
                    env.TEST_FAILED = String.valueOf(failures.toInteger() + errors.toInteger())
                    env.TEST_PASSED = String.valueOf(total.toInteger() - failures.toInteger() - errors.toInteger() - skipped.toInteger())
                    echo "Total: ${env.TEST_TOTAL}, Passed: ${env.TEST_PASSED}, Failed: ${env.TEST_FAILED}"
                }
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
                def total = env.TEST_TOTAL ?: 'N/A'
                def passed = env.TEST_PASSED ?: 'N/A'
                def failed = env.TEST_FAILED ?: 'N/A'
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
