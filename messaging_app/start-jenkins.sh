#!/bin/bash

# Jenkins Docker Setup Script
# This script automates the Jenkins container setup

echo "========================================"
echo "Jenkins Docker Container Setup"
echo "========================================"
echo ""

# Check if Docker is installed
echo "Checking Docker installation..."
if ! command -v docker &> /dev/null; then
    echo "✗ Docker is not installed or not in PATH"
    echo "Please install Docker from: https://www.docker.com/products/docker-desktop"
    exit 1
fi
echo "✓ Docker is installed: $(docker --version)"

# Check if Docker is running
echo "Checking if Docker is running..."
if ! docker ps &> /dev/null; then
    echo "✗ Docker is not running"
    echo "Please start Docker and try again"
    exit 1
fi
echo "✓ Docker is running"

# Check if jenkins container already exists
echo "Checking for existing Jenkins container..."
if [ "$(docker ps -a -q -f name=jenkins)" ]; then
    echo "Jenkins container already exists"
    read -p "Do you want to remove it and create a new one? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Stopping and removing existing container..."
        docker stop jenkins > /dev/null 2>&1
        docker rm jenkins > /dev/null 2>&1
        echo "✓ Existing container removed"
    else
        echo "Starting existing container..."
        docker start jenkins > /dev/null 2>&1
        echo "✓ Jenkins container started"
        echo ""
        echo "Access Jenkins at: http://localhost:8080"
        exit 0
    fi
fi

# Pull Jenkins LTS image
echo "Pulling Jenkins LTS image..."
docker pull jenkins/jenkins:lts

# Run Jenkins container
echo "Starting Jenkins container..."
docker run -d --name jenkins -p 8080:8080 -p 50000:50000 -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts

# Wait for Jenkins to start
echo "Waiting for Jenkins to start (this may take a minute)..."
sleep 30

# Get initial admin password
echo ""
echo "========================================"
echo "Jenkins Setup Information"
echo "========================================"
echo ""
echo "Jenkins URL: http://localhost:8080"
echo ""
echo "Initial Admin Password:"
docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
echo ""
echo "========================================"
echo "Next Steps:"
echo "1. Open http://localhost:8080 in your browser"
echo "2. Copy the password above and paste it in Jenkins"
echo "3. Follow the setup wizard"
echo "4. Refer to JENKINS_SETUP.md for detailed instructions"
echo "========================================"
