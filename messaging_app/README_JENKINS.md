# Jenkins CI/CD Pipeline for Messaging App

This directory contains the Jenkins pipeline configuration for automated testing and continuous integration of the messaging app.

## Quick Start

### Option 1: Automated Setup (Recommended)

**For Windows PowerShell:**
```powershell
.\start-jenkins.ps1
```

**For Git Bash/WSL/Linux:**
```bash
chmod +x start-jenkins.sh
./start-jenkins.sh
```

### Option 2: Manual Setup

Run the following Docker command:
```bash
docker run -d --name jenkins -p 8080:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts
```

Then access Jenkins at: http://localhost:8080

## Files in This Directory

- **Jenkinsfile**: Pipeline script that defines the CI/CD workflow
- **JENKINS_SETUP.md**: Comprehensive setup guide with step-by-step instructions
- **pytest.ini**: Pytest configuration for running tests
- **start-jenkins.ps1**: PowerShell script to automate Jenkins setup (Windows)
- **start-jenkins.sh**: Bash script to automate Jenkins setup (Linux/Mac/Git Bash)
- **requirements.txt**: Python dependencies for the project

## Pipeline Stages

The Jenkins pipeline consists of the following stages:

1. **Checkout**: Pulls the latest code from GitHub
2. **Setup Python Environment**: Creates a virtual environment
3. **Install Dependencies**: Installs required Python packages
4. **Run Tests**: Executes pytest with coverage and reporting
5. **Generate Test Report**: Publishes test results and coverage reports

## Required Jenkins Plugins

- Git Plugin
- Pipeline Plugin
- ShiningPanda Plugin (Python support)
- HTML Publisher Plugin (for test reports)
- JUnit Plugin (for test results)

## GitHub Credentials Setup

Before running the pipeline, you need to add your GitHub credentials to Jenkins:

1. Go to Jenkins → Manage Jenkins → Manage Credentials
2. Add credentials with ID: `github-credentials`
3. Use your GitHub username and Personal Access Token (PAT)

**To create a GitHub PAT:**
1. Go to GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token with `repo` scope
3. Copy the token and use it as the password in Jenkins

## Running the Pipeline

### Manual Trigger
1. Open your Jenkins job
2. Click "Build Now"
3. Monitor the build progress in the console output

### Automatic Trigger (Optional)
Set up a GitHub webhook to trigger builds automatically on push:
1. In GitHub repo: Settings → Webhooks → Add webhook
2. Payload URL: `http://YOUR_JENKINS_URL:8080/github-webhook/`
3. Content type: application/json
4. Events: Just the push event

## Viewing Test Reports

After a successful build, you can view:

- **Test Results**: Click on "Test Result" in the build page
- **Pytest HTML Report**: Click on "Pytest HTML Report" link
- **Coverage Report**: Click on "Coverage Report" link

## Customizing the Pipeline

### Modify Test Execution

Edit the `Jenkinsfile` to customize test execution:

```groovy
pytest --verbose \
       --junit-xml=test-results/junit.xml \
       --html=test-results/report.html \
       --cov=. \
       --cov-report=html
```

### Add Notifications

Add email or Slack notifications in the `post` section:

```groovy
post {
    failure {
        mail to: 'team@example.com',
             subject: "Failed Pipeline: ${currentBuild.fullDisplayName}",
             body: "Something is wrong with ${env.BUILD_URL}"
    }
}
```

### Change Python Version

Modify the `PYTHON_VERSION` environment variable in the Jenkinsfile:

```groovy
environment {
    PYTHON_VERSION = '3.10'
}
```

## Troubleshooting

### Pipeline Fails at Checkout Stage
- Verify GitHub credentials are correctly configured
- Check that the repository URL is correct
- Ensure the branch name is correct (main/master)

### Python Environment Issues
- Install Python in Jenkins container:
  ```bash
  docker exec -u root jenkins apt-get update
  docker exec -u root jenkins apt-get install -y python3 python3-pip python3-venv
  ```

### Test Execution Fails
- Check that all dependencies are in requirements.txt
- Verify test files exist in the specified directory
- Review console output for specific error messages

### Reports Not Showing
- Ensure HTML Publisher plugin is installed
- Check that report files are generated in the correct directory
- Verify file paths in the publishHTML configuration

## Docker Commands Reference

```bash
# View Jenkins logs
docker logs jenkins

# Stop Jenkins
docker stop jenkins

# Start Jenkins
docker start jenkins

# Restart Jenkins
docker restart jenkins

# Remove Jenkins container (data persists in volume)
docker rm jenkins

# Access Jenkins container shell
docker exec -it jenkins /bin/bash

# Get initial admin password
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```

## Additional Resources

- [Complete Setup Guide](JENKINS_SETUP.md)
- [Jenkins Documentation](https://www.jenkins.io/doc/)
- [Jenkins Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [Pytest Documentation](https://docs.pytest.org/)

## Support

For detailed setup instructions, refer to [JENKINS_SETUP.md](JENKINS_SETUP.md).

For issues or questions, please check the troubleshooting section or consult the Jenkins documentation.
