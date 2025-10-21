# Jenkins Pipeline Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Start Jenkins Container

**Windows PowerShell:**
```powershell
.\start-jenkins.ps1
```

**Git Bash/WSL:**
```bash
chmod +x start-jenkins.sh
./start-jenkins.sh
```

**Manual Command:**
```bash
docker run -d --name jenkins -p 8080:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts
```

### Step 2: Access Jenkins & Complete Setup

1. Open browser: **http://localhost:8080**
2. Get password: `docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword`
3. Install suggested plugins
4. Create admin user

### Step 3: Install Required Plugins

Go to: **Manage Jenkins → Manage Plugins → Available**

Install:
- ✅ Git Plugin
- ✅ Pipeline Plugin
- ✅ ShiningPanda Plugin
- ✅ HTML Publisher Plugin
- ✅ JUnit Plugin

## 🔑 Add GitHub Credentials

1. **Manage Jenkins → Manage Credentials → (global) → Add Credentials**
2. Fill in:
   - Kind: Username with password
   - Username: Your GitHub username
   - Password: Your GitHub Personal Access Token
   - ID: `github-credentials`

**Create GitHub PAT:**
- GitHub → Settings → Developer settings → Personal access tokens
- Generate token with `repo` scope

## 📋 Create Pipeline Job

1. **New Item → Enter name: `messaging-app-pipeline` → Pipeline → OK**
2. Configure:
   - **GitHub project**: `https://github.com/YOUR_USERNAME/alx-backend-python`
   - **Pipeline → Definition**: Pipeline script from SCM
   - **SCM**: Git
   - **Repository URL**: `https://github.com/YOUR_USERNAME/alx-backend-python.git`
   - **Credentials**: Select `github-credentials`
   - **Branch**: `*/main`
   - **Script Path**: `messaging_app/Jenkinsfile`
3. **Save**

## ▶️ Run Your First Build

1. Click **"Build Now"**
2. Watch progress in **Console Output**
3. View reports after completion

## 📊 What the Pipeline Does

1. ✅ Checks out code from GitHub
2. ✅ Sets up Python virtual environment
3. ✅ Installs dependencies
4. ✅ Runs pytest tests
5. ✅ Generates HTML reports and coverage

## 🔧 Important Files

- **Jenkinsfile**: Pipeline definition
- **pytest.ini**: Test configuration
- **requirements.txt**: Python dependencies (includes pytest)
- **JENKINS_SETUP.md**: Detailed setup guide
- **README_JENKINS.md**: Complete documentation

## ⚠️ Before First Run

Update Jenkinsfile with your GitHub username:
```groovy
url: 'https://github.com/YOUR_USERNAME/alx-backend-python.git'
```

## 🐛 Common Issues

**Docker not found:**
- Install Docker Desktop
- Restart terminal after installation

**Python not in Jenkins container:**
```bash
docker exec -u root jenkins apt-get update
docker exec -u root jenkins apt-get install -y python3 python3-pip python3-venv
```

**Tests fail:**
- Check requirements.txt has all dependencies
- Verify test files exist
- Check Django settings

## 📚 Need More Help?

- **Detailed Guide**: See [JENKINS_SETUP.md](JENKINS_SETUP.md)
- **Full Documentation**: See [README_JENKINS.md](README_JENKINS.md)
- **Jenkins Docs**: https://www.jenkins.io/doc/

## 🎯 Success Checklist

- [ ] Jenkins running on http://localhost:8080
- [ ] Required plugins installed
- [ ] GitHub credentials added
- [ ] Pipeline job created
- [ ] Jenkinsfile updated with your GitHub username
- [ ] First build successful
- [ ] Test reports visible

---

**Ready to go? Run `.\start-jenkins.ps1` and follow the prompts!**
