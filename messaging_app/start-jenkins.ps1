# Jenkins Docker Setup Script for Windows
# This script automates the Jenkins container setup

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Jenkins Docker Container Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Docker is installed
Write-Host "Checking Docker installation..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version
    Write-Host "✓ Docker is installed: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Docker is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Docker Desktop from: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    exit 1
}

# Check if Docker is running
Write-Host "Checking if Docker is running..." -ForegroundColor Yellow
try {
    docker ps | Out-Null
    Write-Host "✓ Docker is running" -ForegroundColor Green
} catch {
    Write-Host "✗ Docker is not running" -ForegroundColor Red
    Write-Host "Please start Docker Desktop and try again" -ForegroundColor Yellow
    exit 1
}

# Check if jenkins container already exists
Write-Host "Checking for existing Jenkins container..." -ForegroundColor Yellow
$existingContainer = docker ps -a --filter "name=jenkins" --format "{{.Names}}"

if ($existingContainer -eq "jenkins") {
    Write-Host "Jenkins container already exists" -ForegroundColor Yellow
    $response = Read-Host "Do you want to remove it and create a new one? (y/n)"
    if ($response -eq "y" -or $response -eq "Y") {
        Write-Host "Stopping and removing existing container..." -ForegroundColor Yellow
        docker stop jenkins | Out-Null
        docker rm jenkins | Out-Null
        Write-Host "✓ Existing container removed" -ForegroundColor Green
    } else {
        Write-Host "Starting existing container..." -ForegroundColor Yellow
        docker start jenkins | Out-Null
        Write-Host "✓ Jenkins container started" -ForegroundColor Green
        Write-Host ""
        Write-Host "Access Jenkins at: http://localhost:8080" -ForegroundColor Cyan
        exit 0
    }
}

# Pull Jenkins LTS image
Write-Host "Pulling Jenkins LTS image..." -ForegroundColor Yellow
docker pull jenkins/jenkins:lts

# Run Jenkins container
Write-Host "Starting Jenkins container..." -ForegroundColor Yellow
docker run -d --name jenkins -p 8080:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts

# Wait for Jenkins to start
Write-Host "Waiting for Jenkins to start (this may take a minute)..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

# Get initial admin password
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Jenkins Setup Information" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Jenkins URL: http://localhost:8080" -ForegroundColor Green
Write-Host ""
Write-Host "Initial Admin Password:" -ForegroundColor Yellow
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "1. Open http://localhost:8080 in your browser" -ForegroundColor White
Write-Host "2. Copy the password above and paste it in Jenkins" -ForegroundColor White
Write-Host "3. Follow the setup wizard" -ForegroundColor White
Write-Host "4. Refer to JENKINS_SETUP.md for detailed instructions" -ForegroundColor White
Write-Host "========================================" -ForegroundColor Cyan
