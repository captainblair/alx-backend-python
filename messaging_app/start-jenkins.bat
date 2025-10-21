@echo off
REM Jenkins Docker Setup Script for Windows
REM This batch file starts Jenkins in a Docker container

echo ========================================
echo Jenkins Docker Container Setup
echo ========================================
echo.

REM Check if Docker is installed
echo Checking Docker installation...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not installed or not in PATH
    echo Please install Docker Desktop from: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)
echo [OK] Docker is installed

REM Check if Docker is running
echo Checking if Docker is running...
docker ps >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not running
    echo Please start Docker Desktop and try again
    pause
    exit /b 1
)
echo [OK] Docker is running

REM Check if jenkins container already exists
echo Checking for existing Jenkins container...
docker ps -a --filter "name=jenkins" --format "{{.Names}}" | findstr /X jenkins >nul 2>&1
if %errorlevel% equ 0 (
    echo Jenkins container already exists
    set /p response="Do you want to remove it and create a new one? (y/n): "
    if /i "%response%"=="y" (
        echo Stopping and removing existing container...
        docker stop jenkins >nul 2>&1
        docker rm jenkins >nul 2>&1
        echo [OK] Existing container removed
    ) else (
        echo Starting existing container...
        docker start jenkins >nul 2>&1
        echo [OK] Jenkins container started
        echo.
        echo Access Jenkins at: http://localhost:8080
        pause
        exit /b 0
    )
)

REM Pull Jenkins LTS image
echo Pulling Jenkins LTS image...
docker pull jenkins/jenkins:lts

REM Run Jenkins container
echo Starting Jenkins container...
docker run -d --name jenkins -p 8080:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts

REM Wait for Jenkins to start
echo Waiting for Jenkins to start (this may take a minute)...
timeout /t 30 /nobreak >nul

REM Get initial admin password
echo.
echo ========================================
echo Jenkins Setup Information
echo ========================================
echo.
echo Jenkins URL: http://localhost:8080
echo.
echo Initial Admin Password:
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
echo.
echo ========================================
echo Next Steps:
echo 1. Open http://localhost:8080 in your browser
echo 2. Copy the password above and paste it in Jenkins
echo 3. Follow the setup wizard
echo 4. Refer to JENKINS_SETUP.md for detailed instructions
echo ========================================
echo.
pause
