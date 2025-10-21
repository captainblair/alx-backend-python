# Jenkins Setup Guide for Messaging App CI/CD Pipeline

## Prerequisites
- Docker installed and running on your system
- GitHub account with the alx-backend-python repository
- Git installed on your local machine

## Step 1: Run Jenkins in Docker Container

Execute the following command in your terminal (Command Prompt, PowerShell, or Git Bash):

```bash
docker run -d --name jenkins -p 8080:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts
```

**What this command does:**
- `-d`: Runs the container in detached mode (background)
- `--name jenkins`: Names the container "jenkins"
- `-p 8080:8080`: Maps port 8080 (Jenkins web UI)
- `-p 50000:50000`: Maps port 50000 (Jenkins agent communication)
- `-v jenkins_home:/var/jenkins_home`: Creates a persistent volume for Jenkins data
- `jenkins/jenkins:lts`: Uses the Long-Term Support version of Jenkins

**Verify the container is running:**
```bash
docker ps
```

You should see the jenkins container in the list.

## Step 2: Access Jenkins Dashboard

1. Open your web browser and navigate to: `http://localhost:8080`

2. **Get the initial admin password:**
   ```bash
   docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
   ```
   Copy the password displayed in the terminal.

3. Paste the password into the Jenkins unlock screen.

4. Click **"Install suggested plugins"** and wait for the installation to complete.

5. Create your first admin user:
   - Username: (your choice)
   - Password: (your choice)
   - Full name: (your choice)
   - Email: (your email)

6. Click **"Save and Continue"** and then **"Start using Jenkins"**.

## Step 3: Install Required Plugins

1. From the Jenkins dashboard, click **"Manage Jenkins"** → **"Manage Plugins"**.

2. Click on the **"Available"** tab.

3. Search for and install the following plugins:
   - **Git plugin** (usually pre-installed)
   - **Pipeline** (usually pre-installed)
   - **ShiningPanda Plugin** (for Python support)
   - **HTML Publisher Plugin** (for test reports)
   - **JUnit Plugin** (for test results)

4. Check the boxes next to each plugin and click **"Install without restart"**.

5. Wait for the installation to complete.

## Step 4: Add GitHub Credentials

1. From the Jenkins dashboard, click **"Manage Jenkins"** → **"Manage Credentials"**.

2. Click on **(global)** domain.

3. Click **"Add Credentials"** on the left sidebar.

4. Fill in the form:
   - **Kind**: Username with password
   - **Scope**: Global
   - **Username**: Your GitHub username
   - **Password**: Your GitHub Personal Access Token (PAT)
     - To create a PAT: Go to GitHub → Settings → Developer settings → Personal access tokens → Generate new token
     - Required scopes: `repo` (full control of private repositories)
   - **ID**: `github-credentials` (must match the credentialsId in Jenkinsfile)
   - **Description**: GitHub Credentials

5. Click **"Create"**.

## Step 5: Create a New Pipeline Job

1. From the Jenkins dashboard, click **"New Item"**.

2. Enter a name for your job: `messaging-app-pipeline`

3. Select **"Pipeline"** and click **"OK"**.

4. In the job configuration page:

   **General Section:**
   - Check **"GitHub project"** and enter your repository URL:
     `https://github.com/YOUR_USERNAME/alx-backend-python`

   **Build Triggers Section:**
   - Check **"Trigger builds remotely"** (optional, for manual triggers)
   - Or leave unchecked to trigger manually from Jenkins UI

   **Pipeline Section:**
   - **Definition**: Pipeline script from SCM
   - **SCM**: Git
   - **Repository URL**: `https://github.com/YOUR_USERNAME/alx-backend-python.git`
   - **Credentials**: Select the `github-credentials` you created earlier
   - **Branch Specifier**: `*/main` (or your default branch)
   - **Script Path**: `messaging_app/Jenkinsfile`

5. Click **"Save"**.

## Step 6: Update the Jenkinsfile

Before running the pipeline, update the Jenkinsfile with your GitHub repository URL:

1. Open `messaging_app/Jenkinsfile`
2. Replace `YOUR_USERNAME` with your actual GitHub username in the Checkout stage:
   ```groovy
   url: 'https://github.com/YOUR_USERNAME/alx-backend-python.git'
   ```

## Step 7: Run the Pipeline

1. From the pipeline job page, click **"Build Now"**.

2. Watch the pipeline execution in real-time by clicking on the build number (e.g., #1) and then **"Console Output"**.

3. The pipeline will:
   - Checkout code from GitHub
   - Set up a Python virtual environment
   - Install dependencies from requirements.txt
   - Run tests using pytest
   - Generate test reports (JUnit XML, HTML report, coverage report)

4. After completion, view the reports:
   - **Test Results**: Click on "Test Result" in the build page
   - **HTML Report**: Click on "Pytest HTML Report" in the build page
   - **Coverage Report**: Click on "Coverage Report" in the build page

## Troubleshooting

### Issue: Docker command not found
**Solution**: Make sure Docker Desktop is installed and running. Restart your terminal after installation.

### Issue: Jenkins container won't start
**Solution**: 
- Check if port 8080 is already in use: `netstat -ano | findstr :8080`
- Stop any conflicting services or change the port mapping

### Issue: Pipeline fails at Python setup
**Solution**: 
- Ensure Python 3.9+ is installed in the Jenkins container
- You may need to install Python in the container:
  ```bash
  docker exec -u root jenkins apt-get update
  docker exec -u root jenkins apt-get install -y python3 python3-pip python3-venv
  ```

### Issue: Tests fail to run
**Solution**: 
- Check that all dependencies are correctly listed in requirements.txt
- Ensure test files exist in the specified directory
- Verify Django settings are correctly configured

### Issue: GitHub authentication fails
**Solution**: 
- Verify your GitHub Personal Access Token is valid
- Check that the token has the correct permissions (repo scope)
- Ensure the credentialsId in Jenkinsfile matches the ID in Jenkins credentials

## Additional Configuration

### Enable Webhook for Automatic Builds (Optional)

1. In your GitHub repository, go to **Settings** → **Webhooks** → **Add webhook**.

2. Fill in:
   - **Payload URL**: `http://YOUR_JENKINS_URL:8080/github-webhook/`
   - **Content type**: application/json
   - **Events**: Just the push event

3. In Jenkins job configuration, under **Build Triggers**, check:
   - **GitHub hook trigger for GITScm polling**

### Customize Test Reports

You can modify the Jenkinsfile to customize test execution and reporting:
- Add more pytest options
- Configure different coverage thresholds
- Add email notifications on build failure
- Integrate with Slack or other notification services

## Useful Docker Commands

```bash
# View Jenkins logs
docker logs jenkins

# Stop Jenkins container
docker stop jenkins

# Start Jenkins container
docker start jenkins

# Remove Jenkins container (data persists in volume)
docker rm jenkins

# Access Jenkins container shell
docker exec -it jenkins /bin/bash

# Backup Jenkins home directory
docker run --rm -v jenkins_home:/data -v $(pwd):/backup ubuntu tar czf /backup/jenkins_backup.tar.gz /data
```

## Next Steps

- Configure email notifications for build results
- Set up automated builds on Git push (webhooks)
- Add code quality checks (pylint, flake8)
- Integrate with deployment pipelines
- Set up multi-branch pipeline for different branches

## References

- [Jenkins Documentation](https://www.jenkins.io/doc/)
- [Jenkins Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [ShiningPanda Plugin](https://plugins.jenkins.io/shiningpanda/)
- [Docker Jenkins Image](https://hub.docker.com/r/jenkins/jenkins)
