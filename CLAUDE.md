# ceshixuexi — Python 测试 + Jenkins CI 项目

## 项目概要
- **GitHub 仓库**: https://github.com/253765620/ceshixuexi (SSH: git@github.com:253765620/ceshixuexi.git)
- **被测代码**: `calculator.py`（加减乘除、幂运算、奇偶判断）
- **测试用例**: `test_calculator.py`（16 条，pytest）
- **运行测试**: `python -m pytest test_calculator.py -v`

## Jenkins 自动化流水线
- **Jenkins 访问**: http://localhost:8080
- **用户名**: `xzbceshixueixi`
- **任务名称**: `ceshixuexi-pipeline`
- **WAR 包**: `F:\aistudy\jenkins.war`
- **JENKINS_HOME**: `F:\aistudy\jenkins_home`
- **Java 21**: `C:\Program Files\Eclipse Adoptium\jdk-21.0.11.10-hotspot\bin\java`

### 启动 Jenkins
```bash
JENKINS_HOME="F:/aistudy/jenkins_home" \
  "C:/Program Files/Eclipse Adoptium/jdk-21.0.11.10-hotspot/bin/java" \
  -jar "F:/aistudy/jenkins.war" --httpPort=8080
```

### 关闭 Jenkins
```bash
powershell.exe -Command "Stop-Process -Name java -Force"
```

### 流水线配置
- `Jenkinsfile` 定义在仓库根目录
- Poll SCM: 每 2 分钟自动检测 GitHub 新提交并触发构建
- 构建结果通过 **Server酱** 推送到微信
- SendKey: `SCT352402T5740VJf0G3TdpltsoyAGb9pq`

## 流水线阶段
1. Checkout — 从 GitHub 拉代码
2. Install Dependencies — 安装 pytest
3. Run Tests — `pytest -v --junitxml=test-results.xml`
4. Parse Results — 解析 XML 提取测试数据
5. Publish Results — 生成 JUnit 报告
6. Post — Server酱推送微信通知（总计/通过/失败数 + 构建链接）
